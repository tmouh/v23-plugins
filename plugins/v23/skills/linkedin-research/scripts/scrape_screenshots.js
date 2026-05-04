/**
 * LinkedIn Research Agent - Screenshot Capture
 *
 * Vision-based approach: instead of parsing the DOM, we take screenshots of
 * each LinkedIn page and let Claude read them like a human would. No fragile
 * selectors, no text extraction — just images.
 *
 * Usage:
 *   node scrape_screenshots.js <input.json> <screenshots_dir> <pages_csv>
 *
 *   input.json    — { "contacts": [{ "name": "...", "linkedin_url": "..." }] }
 *   screenshots_dir — where to save screenshots (created if it doesn't exist)
 *   pages_csv     — comma-separated pages to visit: main,experience,education,skills,activity,recommendations
 *
 * Output:
 *   <screenshots_dir>/manifest.json — contact list with screenshot paths per contact
 *   <screenshots_dir>/<Name>/main_001.png, experience_001.png, etc.
 */

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

// ─── Config ──────────────────────────────────────────────────────────────────

const CDP_URL = 'http://localhost:9222';
const CONCURRENCY = 5;
const PAGE_LOAD_WAIT = 3000;   // ms after navigation before screenshotting
const SCROLL_STEP = 900;       // px per scroll increment
const SCROLL_WAIT = 700;       // ms between scrolls (let lazy content load)
const MAX_SCREENSHOTS = 10;    // per page — safety cap
const VIEWPORT = { width: 1920, height: 1080 };

// Pages we know about and what URL pattern links to them from the main profile
const KNOWN_SUBPAGES = {
  experience:      href => href.includes('/details/experience'),
  education:       href => href.includes('/details/education'),
  skills:          href => href.includes('/details/skills'),
  activity:        href => href.includes('/recent-activity'),
  recommendations: href => href.includes('/details/recommendations'),
};

// ─── Utilities ────────────────────────────────────────────────────────────────

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function sanitizeName(name) {
  return name.replace(/[^a-zA-Z0-9_\- ]/g, '').replace(/\s+/g, '_').substring(0, 60);
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// ─── Window maximize ─────────────────────────────────────────────────────────

async function maximizeWindow(page) {
  try {
    const session = await page.target().createCDPSession();
    const { windowId } = await session.send('Browser.getWindowForTarget');
    await session.send('Browser.setWindowBounds', {
      windowId,
      bounds: { windowState: 'maximized' }
    });
    await session.detach();
    console.log('  Chrome window maximized');
  } catch (e) {
    // Not fatal — viewport is still set to 1920x1080
    console.log(`  Window maximize skipped (${e.message}) — viewport set to ${VIEWPORT.width}x${VIEWPORT.height}`);
  }
}

// ─── Page status checks ──────────────────────────────────────────────────────

async function checkPageStatus(page) {
  const url = page.url();
  if (url.includes('/login') || url.includes('/authwall') || url.includes('/checkpoint')) {
    return 'AUTH_REQUIRED';
  }
  try {
    const text = await page.evaluate(() => document.body.innerText.substring(0, 600));
    if (
      text.includes("This page doesn't exist") ||
      text.includes("This page doesn\u2019t exist") ||
      text.includes("Page not found") ||
      text.includes("profile isn't available")
    ) {
      return 'PROFILE_NOT_FOUND';
    }
  } catch {}
  return null;
}

// ─── Sub-page link finder ────────────────────────────────────────────────────
// We find links to sub-pages by reading href attributes — this is just
// navigation, not content extraction. Completely resistant to DOM structure changes.

async function findSubPageLinks(page, wantedPages) {
  const links = {};
  try {
    const found = await page.evaluate((knownPatterns) => {
      const result = {};
      const anchors = Array.from(document.querySelectorAll('a[href]'));
      for (const a of anchors) {
        const href = a.href || '';
        if (!href.includes('linkedin.com')) continue;
        for (const [key, pattern] of Object.entries(knownPatterns)) {
          if (!result[key] && pattern.test(href)) {
            // Strip query params for cleanliness
            result[key] = href.split('?')[0].replace(/\/$/, '') + '/';
          }
        }
      }
      return result;
    }, {
      experience:      /\/details\/experience/,
      education:       /\/details\/education/,
      skills:          /\/details\/skills/,
      activity:        /\/recent-activity/,
      recommendations: /\/details\/recommendations/,
    });

    for (const page of wantedPages) {
      if (found[page]) links[page] = found[page];
    }
  } catch (e) {
    console.warn(`  Link finder error: ${e.message}`);
  }
  return links;
}

// ─── Screenshot a page (scroll-and-capture) ──────────────────────────────────

async function screenshotPage(page, outputDir, prefix) {
  const screenshots = [];
  await page.setViewport(VIEWPORT);

  // Scroll to top
  await page.evaluate(() => window.scrollTo(0, 0));
  await sleep(500);

  let scrollY = 0;
  let num = 1;

  while (num <= MAX_SCREENSHOTS) {
    const filename = `${prefix}_${String(num).padStart(3, '0')}.png`;
    const filepath = path.join(outputDir, filename);

    await page.screenshot({ path: filepath, fullPage: false });
    screenshots.push(filepath);

    // Check if we've reached the bottom
    const { scrollHeight, clientHeight, currentScrollY } = await page.evaluate(() => ({
      scrollHeight: document.body.scrollHeight,
      clientHeight: window.innerHeight,
      currentScrollY: window.scrollY,
    }));

    if (currentScrollY + clientHeight >= scrollHeight - 50) break; // at the bottom

    // Scroll down
    scrollY += SCROLL_STEP;
    await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), scrollY);
    await sleep(SCROLL_WAIT);
    num++;
  }

  return screenshots;
}

// ─── Profile scraper ─────────────────────────────────────────────────────────

async function scrapeProfile(browser, contact, pagesToVisit, screenshotsDir) {
  const contactDir = path.join(screenshotsDir, sanitizeName(contact.name));
  ensureDir(contactDir);

  const result = {
    name: contact.name,
    linkedin_url: contact.linkedin_url,
    status: 'success',
    error: null,
    screenshots: {},
  };

  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);

  try {
    // ── Step 1: Load main profile ─────────────────────────────────────────
    console.log(`  [${contact.name}] Loading profile...`);
    await page.goto(contact.linkedin_url, {
      waitUntil: 'domcontentloaded',
      timeout: 20000,
    });
    await sleep(PAGE_LOAD_WAIT);

    const statusErr = await checkPageStatus(page);
    if (statusErr) {
      result.status = statusErr;
      result.error = statusErr;
      console.log(`  [${contact.name}] ✗ ${statusErr}`);
      await page.close();
      return result;
    }

    // Maximize window on first profile (persists for the session)
    if (contact._first) await maximizeWindow(page);

    // ── Step 2: Screenshot main profile ──────────────────────────────────
    if (pagesToVisit.includes('main')) {
      console.log(`  [${contact.name}] Screenshotting main profile...`);
      const shots = await screenshotPage(page, contactDir, 'main');
      result.screenshots.main = shots;
      console.log(`  [${contact.name}] main → ${shots.length} screenshots`);
    }

    // ── Step 3: Find sub-page links ───────────────────────────────────────
    const subPages = pagesToVisit.filter(p => p !== 'main');
    let subPageLinks = {};

    if (subPages.length > 0) {
      // Scroll back to top so all anchor tags are accessible
      await page.evaluate(() => window.scrollTo(0, 0));
      await sleep(300);
      subPageLinks = await findSubPageLinks(page, subPages);

      const found = Object.keys(subPageLinks);
      const missing = subPages.filter(p => !found.includes(p));
      if (found.length > 0) console.log(`  [${contact.name}] Found sub-page links: ${found.join(', ')}`);
      if (missing.length > 0) console.log(`  [${contact.name}] Sub-page links not found on profile: ${missing.join(', ')} (will skip)`);
    }

    // ── Step 4: Screenshot each sub-page ─────────────────────────────────
    for (const pageKey of subPages) {
      const url = subPageLinks[pageKey];
      if (!url) continue;

      console.log(`  [${contact.name}] Navigating to ${pageKey} (${url})...`);
      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
        await sleep(PAGE_LOAD_WAIT);

        const err = await checkPageStatus(page);
        if (err) {
          console.log(`  [${contact.name}] ${pageKey} page: ${err}`);
          continue;
        }

        const shots = await screenshotPage(page, contactDir, pageKey);
        result.screenshots[pageKey] = shots;
        console.log(`  [${contact.name}] ${pageKey} → ${shots.length} screenshots`);
      } catch (e) {
        console.warn(`  [${contact.name}] ${pageKey} page error: ${e.message}`);
      }
    }

    const totalShots = Object.values(result.screenshots).flat().length;
    console.log(`  [${contact.name}] ✓ Done — ${totalShots} total screenshots`);

  } catch (e) {
    result.status = 'error';
    result.error = e.message;
    console.error(`  [${contact.name}] ✗ Error: ${e.message}`);
  } finally {
    try { await page.close(); } catch {}
  }

  return result;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const [,, inputPath, screenshotsDir, pagesCsv] = process.argv;

  if (!inputPath || !screenshotsDir || !pagesCsv) {
    console.error('Usage: node scrape_screenshots.js <input.json> <screenshots_dir> <pages_csv>');
    console.error('  pages_csv: comma-separated list — e.g. "main,experience,education"');
    process.exit(1);
  }

  const input = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const contacts = (input.contacts || []).filter(c => c.linkedin_url);
  const pagesToVisit = pagesCsv.split(',').map(p => p.trim()).filter(Boolean);

  if (!contacts.length) {
    console.error('No contacts with linkedin_url found in input');
    process.exit(1);
  }

  ensureDir(screenshotsDir);

  // Remove any stale manifest from a previous run
  const manifestPath = path.join(screenshotsDir, 'manifest.json');
  if (fs.existsSync(manifestPath)) fs.unlinkSync(manifestPath);

  console.log(`\nLinkedIn Research Agent`);
  console.log(`Contacts: ${contacts.length}`);
  console.log(`Pages:    ${pagesToVisit.join(', ')}`);
  console.log(`Output:   ${screenshotsDir}`);
  console.log(`─────────────────────────────────────`);

  // Mark first contact so we maximize the window once
  if (contacts.length > 0) contacts[0]._first = true;

  const browser = await puppeteer.connect({ browserURL: CDP_URL });

  const results = [];
  const startTime = Date.now();

  // Process in batches of CONCURRENCY
  for (let i = 0; i < contacts.length; i += CONCURRENCY) {
    const batch = contacts.slice(i, i + CONCURRENCY);
    const batchNum = Math.floor(i / CONCURRENCY) + 1;
    const totalBatches = Math.ceil(contacts.length / CONCURRENCY);
    console.log(`\nBatch ${batchNum}/${totalBatches}: ${batch.map(c => c.name).join(', ')}`);

    const batchResults = await Promise.all(
      batch.map(c => scrapeProfile(browser, c, pagesToVisit, screenshotsDir))
    );
    results.push(...batchResults);

    // Brief pause between batches to avoid rate-limiting
    if (i + CONCURRENCY < contacts.length) {
      await sleep(2000);
    }
  }

  const duration = ((Date.now() - startTime) / 1000).toFixed(1);
  const success = results.filter(r => r.status === 'success').length;
  const failed = results.filter(r => r.status !== 'success').length;

  // Write manifest — Claude will read this to know which screenshots exist per contact
  const manifest = {
    captured_at: new Date().toISOString(),
    duration_seconds: parseFloat(duration),
    pages_visited: pagesToVisit,
    stats: { total: contacts.length, success, failed },
    contacts: results.map(r => ({
      name: r.name,
      linkedin_url: r.linkedin_url,
      status: r.status,
      error: r.error,
      screenshot_dir: path.join(screenshotsDir, sanitizeName(r.name)),
      screenshots: r.screenshots,
    })),
  };

  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), 'utf8');

  console.log(`\n─────────────────────────────────────`);
  console.log(`Done in ${duration}s — ${success}/${contacts.length} succeeded`);
  if (failed > 0) {
    results.filter(r => r.status !== 'success').forEach(r => {
      console.log(`  ✗ ${r.name}: ${r.error}`);
    });
  }
  console.log(`Manifest: ${manifestPath}`);

  process.exit(0);
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
