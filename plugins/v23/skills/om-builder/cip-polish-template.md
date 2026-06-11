# CIP Polish — Shape-Level Punch-List Template

**OPTIONAL. POST-PHASE-5 ONLY. NEVER ON THE CRITICAL PATH.**

Claude Code has already built the deck via `build-deck.py` and passed it through Phase 5 QA (visual render loop + verification + editorial gate). The `.pptx` is structurally complete, in-voice, and numerically verified. CIP's role here is bounded: execute a pre-specified visual punch-list against named shapes. CIP does not author, recompose, rewrite prose, re-derive numbers, or touch slides that are already complete. If you spot a content error, flag it — do not silently edit.

---

## How to use this template

1. After Phase 5 QA passes, identify the bounded set of shape-level visual actions that remain (typically: swap a cover photo placeholder for the supplied image; annotate an aerial; place a logo at an exact position).
2. Fill in the punch-list below — one item per action. Every item must have a precondition; if the precondition fails, CIP skips and reports, it does not improvise.
3. Deliver to CIP as a self-contained paste block. CIP has no memory across turns — re-deliver the full block each session.

---

## Punch-list item format

```
### Item N — [one-line description]
**Target:** Slide [number] — shape name "[SHAPE_NAME]" (shape ID: [id if known])
**Precondition:** [what must be true before touching it; e.g., "shape exists and its text reads exactly '[COVER_PHOTO_PLACEHOLDER]'"]
**Action (verbatim):** [exact instruction — text to set, image to place, geometry to apply]
  - If inserting an image: source URI = [Microsoft Graph resource URI or SharePoint path]; crop = [none / fill / exact dimensions w=X" h=Y"]; position = x=[X]" y=[Y]" from top-left of slide
  - If setting text: set text to exactly: "[verbatim text — no paraphrase]"
  - If adjusting geometry: set left=[X]" top=[Y]" width=[W]" height=[H]"
**Skip rule:** If the precondition fails (shape absent, or text does not match), skip this item, log "SKIPPED — Item N: [reason]", and continue to Item N+1. Do not improvise an alternative.
```

---

## Example items (filled)

### Item 1 — Swap cover photo placeholder for supplied aerial
**Target:** Slide 1 — shape name "CoverPhoto" (shape ID: 2)
**Precondition:** Shape exists and contains the text label "[COVER_PHOTO_PLACEHOLDER]"
**Action (verbatim):** Replace the placeholder picture frame with the image at the following SharePoint URI: `[INSERT GRAPH URI HERE]`. Position: x=0.0" y=0.0" width=6.83" height=7.5" (left-half full-bleed, no rounded corners, aspect-ratio fill). Remove the placeholder label text after placement.
**Skip rule:** If shape "CoverPhoto" is absent or contains different text, skip and report "SKIPPED — Item 1: cover placeholder not found."

---

### Item 2 — Place annotated aerial on map slide placeholder
**Target:** Slide [N] — shape name "MapPlaceholder" (look up shape ID from the inventory file at `x V23\<deal>-extracted\inventory.txt`)
**Precondition:** Shape exists and contains the text label "[MAP_PLACEHOLDER — annotated aerial with property pin]"
**Action (verbatim):** Place the aerial image at `[INSERT GRAPH URI HERE]` into this placeholder. Position: x=0.87" y=1.05" width=9.38" height=5.92". After placing the image, add a numbered oval pin shape (circle, navy fill #1F3A5F, 0.25" diameter) at the property location — coordinates approximately x=5.1" y=3.2" (adjust if the property falls at a visually different position on the aerial). Add a text label "1" inside the oval, Garamond 10pt bold white. Do not add any additional annotation shapes; the surrounding slide text is already in place.
**Skip rule:** If "MapPlaceholder" is absent or the aerial URI fails to load, skip and report "SKIPPED — Item 2: [specific reason]."

---

### Item 3 — Place sponsor logo on cover slide
**Target:** Slide 1 — sponsor logo zone (shape name "SponsorLogoPlaceholder")
**Precondition:** Shape exists and contains the text "[SPONSOR_LOGO_PLACEHOLDER]"
**Action (verbatim):** Place the sponsor logo image at `[INSERT GRAPH URI HERE]` at position x=10.74" y=6.0" width=2.06" height=0.85". Do not apply any border, shadow, or rounding. Remove the placeholder text after placement.
**Skip rule:** If the URI fails or the shape is absent, leave the placeholder label in place and report "SKIPPED — Item 3: sponsor logo placement failed."

---

## Closing instructions

After completing all items (or skipping those whose preconditions failed):

1. Report per-item status in order: **DONE** or **SKIPPED — [reason]**.
2. Do not declare the deck "complete" until you have reported every item.
3. If any image insertion failed (Step 11 operational rule: raster insertion is not guaranteed), list the failed assets explicitly so the user can insert them manually.
4. Save the file. Do not overwrite a different version — confirm the target filename before saving.

---

## Operational caveats (Office.js — applies to bounded shape edits only)

These are the caveats relevant to the narrow punch-list scope (not composition machinery, which is already handled by Claude Code).

**Font embedding:** Garamond and Bell MT must be embedded in the `.pptx` before CIP touches it — unembedded fonts can silently substitute to Calibri on non-Windows machines. Verify via File → Info → Inspect Document → Embedded Fonts before starting. If either font is missing, do not proceed; surface to the user.

**Shape z-order after image insertion:** When placing an image over a placeholder frame, the image may land behind the existing text labels (eyebrow / title / takeaway). After placement, confirm the image is behind the text shapes by checking z-order. If the text is obscured, send the image to back (`Selection.ShapeRange.ZOrder(msoSendToBack)`). Do not rearrange any other z-order.

**Text-range vs. shape operations:** For text edits, target the shape's `TextRange` (`shape.TextFrame2.TextRange.Text`), not the shape itself. Replacing `Shape.TextFrame.Text` can strip run-level formatting (bold inline numerics, font size). Use `getSubstring` for sub-range edits where formatting must be preserved.

**`&` in text:** Escape ampersands as `&amp;` in any XML you write. Unescaped `&` in shape text or Open XML payloads corrupts the slide.

**Shape IDs shift after structural edits:** Re-list shapes via the inventory before each item if a prior item deleted or added a shape.

**Batch, don't dribble:** Fold all of one item's actions into a single batch. Multiple tiny single-edit turns are slow and quota-expensive.
