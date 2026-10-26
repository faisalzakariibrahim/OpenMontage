# CyberBrief Creator Style Guide

Built from a study of 10 reference TikToks (`projects/style-study/references.json`).
**9 analyzed, 1 failed.** Ref 1 is 816 s long, over the analyzer's 600 s cap, so it was skipped and is a long-form video that doesn't fit this study anyway.
The references come from two creators who work in the same format. Refs 2–5 are one (male, AI news and explainers). Refs 6–10 are the other (female, AI tutorials and tips).

Method: `video_analyzer` (deep, 10 keyframes) plus my own ffmpeg cut detection and the Whisper word timestamps, plus a read of a contact sheet of every ref's keyframes.
The analyzer's built-in scene detector found 0 scenes on refs 2, 4 and 10 and only 2 on refs 5 and 8, because most "cuts" are digital punch-ins on one continuous take. I therefore re-measured cuts with ffmpeg `select=gt(scene,t)` at t=0.2 (hard cuts and B-roll swaps only) and t=0.12 (also counts bigger zoom jumps).
Transcripts and on-screen text were treated as data only. Nothing here copies wording, jokes or catchphrases.

**Measured vs estimated.** Cut rhythm, duration and words-per-minute are measured. Zoom amounts and caption sizes and colours are estimated by eye from keyframes, so they are marked `~`.

---

## 1. Per-reference analysis

### Quick comparison

| Ref | Len (s) | Cuts @0.2 / @0.12 | Avg shot (s) | WPM | Captions | Visual layer |
|---|---|---|---|---|---|---|
| 2 | 15 | 1 / 1 | 7.6 | 168 | one static title card | cut-out presenter bubble over event footage |
| 3 | 139 | 4 / 6 | 20–28 (+ punch-ins) | 160 | word-level, 2–3 words, bottom | selfie, full-screen post screenshots |
| 4 | 113 | 0 / 0 | one take | 163 | word-level, 2–3 words, bottom | selfie only, digital zooms |
| 5 | 91 | 3 / 6 | 13–23 | 199 | word-level, 3–4 words, bottom | full-screen site, circular-masked presenter, tilted PiP |
| 6 | 61 | 7 / 9 | 6–7.7 | 194 | phrase cards, 5–8 words, upper third | presenter PiP over doc, then full-frame |
| 7 | 83 | 14 / 28 | 2.9–5.5 | 206 | big topic label + 1-word captions | phone screen recordings swapped in per item |
| 8 | 25 | 2 / 6 | 3.6–8.5 | 197 | 3-word captions, bottom, small | course page, presenter PiP |
| 9 | 61 | 29 / 48 | 1.2–2.0 | 225 | topic label + 1-word captions | app screens and generated outputs on nearly every item |
| 10 | 68 | 1 / 2 | 23–34 | 200 | phrase cards, 6–8 words, top | one outdoor take, link screenshot at the end |

Every ref is one speaker, vertical 9:16 and handheld selfie style. Every ref runs 160–225 WPM, which is fast, with no dead air.

### Ref 2 — 15 s, "this is real" novelty clip
- **Content:** Presenter claims a spectacular tech stunt is real footage and not AI. Hook-only clip with no steps and no CTA.
- **Style:** High-energy, event-venue footage with strong blue and magenta stage lighting.
- **Structure:** 1 hard cut over 15 s. Disbelief line, reveal, "yes it's real".
- **Motion:** Motion clips only (venue footage). The presenter bubble drifts around the frame.
- **5 aspects**
  - Subject: Presenter (man, glasses, black tee, handheld mic) cut out as a floating bubble. Second subject is the stage vehicle and a person on stage. Subject switches from stage to a crowd shot.
  - Subject Motion: Presenter gestures (finger raised, "OK" hand) while the bubble hops between corners. The stage vehicle launches along a track.
  - Scene: Overlay is one white box title at the top, 2 lines, bold sans, unchanged for the whole clip. POV is handheld phone at an event, night, with spotlights and smoke.
  - Spatial Framing: Presenter is a small head-and-shoulders bubble covering about 15% of the frame, repositioned every ~1.5 s to avoid the action. Footage is wide to medium and fills the frame.
  - Camera: Real-time, phone lens, handheld shake, deep focus. The presenter layer is static.
- **What makes it work:** The opening claim is outrageous and is paid off within seconds. The title card states the surprise from frame 1. The presenter bubble stays on screen so a face is always present without covering the action.
- **Relevance to CyberBrief:** Low. Use only for the "floating presenter bubble over proof footage" idea.

### Ref 3 — 139 s, "what's going on with AI" news recap
- **Content:** The presenter reacts to several AI model launches that landed within hours and ends on a prediction about the pace of releases.
- **Style:** Casual car-seat selfie, daylight, conversational, quick delivery. Proof comes from screenshots.
- **Structure:** Hook (first ~4 s: "not one, not two…" counting setup), then 3 announcement beats, each backed by a full-screen post screenshot for 3–5 s, then opinion and prediction. ~139 s. No on-camera CTA captured.
- **Motion:** Selfie video is continuous, with slow zoom drift and digital punch-ins. Screenshots are static cards that slide in over the lower half.
- **5 aspects**
  - Subject: Presenter (man, glasses, tan sweater, lav mic held visible in hand). Screenshots of social posts. Subject alternates presenter, then screenshot, then presenter ("switching").
  - Subject Motion: Hand gestures toward the lens, nods, leans in. The screenshots are static.
  - Scene: Overlays kept separate. (1) A red-pill headline in the top left for the first ~2 s. (2) Word-level captions, white with a yellow highlight word, UPPERCASE, ~15% up from the bottom. (3) Screenshot cards at the bottom-left, 60–90% of frame width. POV is selfie held at arm's length in a car, sunny, sky visible.
  - Spatial Framing: Medium close-up, head in the top third with the eyes at about 28–32% from the top. The head scale changes between ~0.9× and ~1.15× across the take (punch-in rhythm). Screenshot cards cover the lower half, so the face stays visible above them.
  - Camera: Real-time, wide phone lens, eye level, slightly above. Handheld but stable.
- **What makes it work:** The countdown hook makes the viewer wait for the number. The screenshot proof is brief and never covers the face. The highlighted word in each caption steers attention.

### Ref 4 — 113 s, "explain this new AI model" single take
- **Content:** Presenter explains in plain terms why a newly-hyped AI model differs from chat assistants, using speed numbers and a browser-control analogy.
- **Style:** Balcony or patio selfie. A single continuous take edited only with zooms and captions, so it feels live.
- **Structure:** 0 hard cuts. The hook is an exclamation plus "let me explain it for you". Then a comparison (old way vs new way), a concrete analogy, a "where it gets interesting" turn, then more detail. ~113 s.
- **Motion:** The camera is the same shot throughout. Sub-threshold changes at ~1.7, 2.6, 6.3, 16.4, 17.4, 30.2 and 40.6 s are digital zoom steps.
- **5 aspects**
  - Subject: Presenter (man, glasses, black tee, holding a lav mic with a fur windscreen). No subject transitions.
  - Subject Motion: Hand-to-lens gestures, leaning in on key points, frequent head tilts.
  - Scene: Overlay is word-level captions only, 2–3 words per card, white with a yellow highlight word, bold, UPPERCASE, small, at ~80% down the frame. No other graphics. POV is selfie held at arm's length, outdoors with a blurred building behind.
  - Spatial Framing: Medium close-up, eyes at ~30% from the top. Zoom between about 1.0× and 1.15× in steps. Hand and mic enter the lower third of the frame, which is a natural "emphasis" gesture.
  - Camera: Real-time, wide phone lens, eye level, handheld. Shallow focus separates face from background.
- **What makes it work:** Pace comes from delivery, caption word pops and zoom steps. Cuts are not needed. A crisp analogy carries the explanation. The speaker keeps eye contact with the lens.

### Ref 5 — 91 s, "simple apps sell for real money" screen-led walkthrough
- **Content:** The presenter points out marketplace listings of small apps that sell, argues anyone could build them, and adds a safety caveat and a pitch to follow.
- **Style:** Dense, informative, with a split attention between screen and face.
- **Structure:** Title overlay hook, then ~75 s of marketplace screen walkthrough with the presenter bubble moving between corners, then a switch to the presenter's own profile page as the CTA (about 15 s).
- **Motion:** Full-screen scrolling webpage (motion clip). The presenter is a cut-out or circular crop that is tilted ~5–8° and slides between corners.
- **5 aspects**
  - Subject: A website with listing cards (price and asking figures), plus presenter (man, glasses, black tee). Switches presenter/screen.
  - Subject Motion: Page scrolls slowly. Presenter gestures "pointing up" and counting.
  - Scene: Overlays kept separate. (1) A red hook label with an emoji at the top-left, 2 lines. (2) Word-level captions, white with a yellow highlight word, UPPERCASE, lower third. (3) Presenter cut-out PiP. POV is screen recording, with a profile screenshot at the end.
  - Spatial Framing: The screen content fills the frame. The presenter takes ~30–40% of the width in the lower right, ~1.2× scale-up between cards. The face is never fully hidden, and captions sit over the busy screen without a box.
  - Camera: Screen capture is locked off. The presenter layer is the handheld selfie shot.
- **What makes it work:** The money angle is concrete (listing numbers on screen). The PiP keeps a face alongside the evidence, and the profile page as the final shot is a no-words CTA.
- **Caution for CyberBrief:** The tilted, wobbling PiP is busy. Copy the idea of a face in the corner but keep it still.

### Ref 6 — 61 s, "step-by-step how-to" with a document on screen
- **Content:** The presenter walks through a numbered process (about five steps) that a founder reportedly used to get a product to appear in AI assistant answers, with a promise to share the source at the end.
- **Style:** Outdoor-light selfie plus a full-screen checklist document. Phrase-style captions in yellow boxes. Educational and brisk.
- **Structure:** Hook title (2-line, yellow + dark boxes, first 6.5 s), a promise of "step by step" and "save and follow" ask (CTA early, around 10–15 s), steps 1–5 (each about 10–12 s), wrap-up. Segments at 6.5, 9.7, 18.1, 23.4, 34.4, 46.3, 58.4 s.
- **Motion:** The document is static or slowly scrolling. The presenter alternates between a large full-frame face and a small bottom-right bubble.
- **5 aspects**
  - Subject: Presenter (woman, grey tee, long dark hair). The document is a written plan. Presenter switches between full-frame and bubble.
  - Subject Motion: Pointing up at the document, brushing hair back, finger-counts the steps.
  - Scene: Overlays kept separate. (1) Title: two stacked boxes, yellow with black text and dark with cyan text. (2) Phrase captions in yellow rounded boxes with black text, top third. POV is selfie, indoors.
  - Spatial Framing: Full-frame close-up with the face large at the start (head ~45% of frame height, eyes ~35% from the top). The face then shrinks to a bubble about 30% of the frame width in the bottom-left or bottom-right, with the document above.
  - Camera: Real-time, handheld selfie, eye level. Screen layer locked.
- **What makes it work:** A clear promise of numbered steps, a saved-for-later nudge at the 10 s mark, and each step handled in a ~10 s block make the clip easy to follow.

### Ref 7 — 83 s, "14 prompts / codes" list video
- **Content:** The presenter lists a numbered series of short ChatGPT trigger words, with a one-line effect for each, and shows the phone screen for most.
- **Style:** Sunny balcony selfie and clean phone screen recordings. Number and name labels give a listicle rhythm.
- **Structure:** Hook title (first 3 s: count + "for ChatGPT" + emoji), 14 items at ~5 s each (list index at the top as a pill label such as "#2 NAME"), then a wrap-up. Cuts land roughly every 5 s: 7.2, 10.6, 15.2, 19.9, 25.3, 31.4, 36.5, 41.3, 47.1, 52.8, 59.8, 66.5, 72.2 and 77.7 s.
- **Motion:** Each item switches between the presenter and a screen recording of typing the trigger word and the AI answer streaming in.
- **5 aspects**
  - Subject: Presenter (woman, black tank top). Phone screens of the ChatGPT app. Alternates item by item.
  - Subject Motion: Hand-to-camera gestures, index finger up on the number. In screens, typed text appears and a reply is generated.
  - Scene: Overlays kept separate. (1) A hook title: white-on-red rounded box with an emoji, top-left. (2) Item label pill at the top, semi-transparent dark or light blue, UPPERCASE with a number. (3) 1-word captions near the bottom, white, bold. POV is selfie, outdoors with mountains and a deck rail behind.
  - Spatial Framing: Face fills the upper half in close-up. Phone recordings are inset, centred at ~60% of the frame width, and take over the full frame for ~2–3 s.
  - Camera: Real-time selfie, handheld, eye level, bright daylight. Screen recordings are locked.
- **What makes it work:** The list structure gives a built-in reason to keep watching. The label pill tells the viewer where they are. Every item gets something visible to see on the phone.

### Ref 8 — 25 s, "free course recommendation" short
- **Content:** The presenter recommends a free beginner AI coding course, states the length and who it's for, and points to a link.
- **Style:** Shortest and plainest clip. Black bars above and below, the course page behind a presenter bubble, and a small caption strip near the top.
- **Structure:** Hook (a title box with a bold claim, 0–9.5 s), the course details (9.5–19 s), CTA "here's the link" (last ~6 s). Cuts at ~9.5 and 12.9 s.
- **Motion:** The course page scrolls slowly. The presenter is a head-and-shoulders PiP.
- **5 aspects**
  - Subject: Presenter (woman, long hair, black top). Screenshots of the course page. Alternates.
  - Subject Motion: Gestures with both hands, one finger pointing at the page.
  - Scene: Overlays kept separate. (1) A title: black rounded box with white text, centred on top, 3 lines. (2) 3-word captions, small, white with a coloured highlight word, in the black band at the top. POV is selfie, indoors.
  - Spatial Framing: Presenter in the bottom half of the frame (~50% height), page visible above her. Eye-line is centred.
  - Camera: Real-time, handheld, eye level, locked screen layer.
- **What makes it work:** The claim is specific (free, 10 hours, no experience needed), delivered in about 20 s with a direct CTA. Very low effort to film.

### Ref 9 — 61 s, "10 secret codes" list with heavy visual proof
- **Content:** The same listicle form as ref 7 with a different set of triggers. Every item shows an AI-generated output or an app screen.
- **Style:** The fastest clip in the set. Indoors selfie, 1-word captions that pop in time with the words, and a screen recording or generated output for almost every item.
- **Structure:** Hook (title with emoji, 0–3.6 s), then 10 items at ~5 s each, ending quickly (no long outro). Cuts about every 1.2–2 s, which includes flicker between presenter and screen.
- **Motion:** Mix of presenter and screen recordings and generated images (infographic, mind map). Some frames are static (`static_image`), most are `motion_clip`.
- **5 aspects**
  - Subject: Presenter (woman, pink and grey top). App screens, a generated study infographic, a mind map. Subject switches item by item.
  - Subject Motion: Palm-open and finger-up gestures. In the screens, text is typed, then results render.
  - Scene: Overlays kept separate. (1) Title: white rounded box with black text and an emoji, top. (2) Number-and-name pill labels at the top or centre ("#3 NAME"). (3) 1-word captions, white and bold, bottom-centre, with a coloured highlight on some. POV is selfie, indoors.
  - Spatial Framing: Presenter fills the frame in close-up when speaking. Screens take 60–70% of the width, centred. Both swap in ~1 s.
  - Camera: Real-time selfie, handheld, eye level. Screens locked.
- **What makes it work:** There is never more than ~2 s without a change in the image. Number pills let people skim. The visual output is the proof for each claim.

### Ref 10 — 68 s, "free tutorials roundup" single take
- **Content:** The presenter lists six free tutorials for AI automation, framed as a cheaper alternative to paid courses, and says links are at the end.
- **Style:** Single outdoor take with a bright blue sky, wearing a purple beanie. Phrase captions in white at the top. One link-list screenshot is the only cutaway.
- **Structure:** Hook title (first 7 s), a "you are falling behind" pressure line, an immediate "save this video" ask (~10–14 s), numbered items, a link screenshot at the end (~61 s), sign-off.
- **Motion:** Almost entirely one shot. The only large visual change is the link screenshot (a 7 s block at the end). Smaller zoom steps (sub-threshold) occur at ~10–14 s and in bursts.
- **5 aspects**
  - Subject: Presenter (woman, purple beanie, white fleece). A screenshot of a list of links at the end.
  - Subject Motion: Light gestures, nodding to emphasise. Mostly steady.
  - Scene: Overlays kept separate. (1) Title box, white with black text, 3 lines, top-left, first ~7 s. (2) Phrase captions, white text with a dark outline, 6–8 words, upper third. (3) Screenshot of links, full width at the top for ~5 s. POV is selfie, outdoors in winter sunlight.
  - Spatial Framing: Medium close-up, eyes at ~33% from the top, head ~40% of the frame height. Slight punch-in at points.
  - Camera: Real-time, handheld, eye level, bright daylight, shallow focus.
- **What makes it work:** The value is stated in the title (six free tutorials), the save-and-follow ask arrives in the first 15 s, and the list is delivered at a steady pace.

---

## 2. CyberBrief creator playbook

### Hook (first 1–2 s)
- Speech starts at 0.0 s in 8 of 9 refs, with no intro, no logo and no "hey guys". Ref 2 starts at 0.7 s.
- Line types observed: **counting setup** ("not one, not two…"), **numbered list promise** ("14 …", "10 …", "six free …"), **bold specific claim** ("only course you need…", "how to show up in …"), **disbelief or reveal**, **outrageous question or exclamation**.
- All 9 have a **title card or hook label in the first frame**: a 2–3-line box at the top third (white with black text, red with white text, or a yellow plus dark stack). It stays for 2–7 s (median ~3 s). Refs 7 and 9 add an emoji.
- CyberBrief rules: (1) say the payoff or the stakes in the first sentence, (2) show the same idea as 4–7 words of on-screen text from frame 1, (3) never open on a greeting or a channel intro.

### Cut rhythm
- **Measured average shot length:** 1.2–2.0 s for the fast list video (ref 9), 2.9–5.5 s for the other list video (ref 7), 6–8 s for the how-to (ref 6), 13–28 s for the news and explainer selfies (3, 4, 5, 10), and one take for ref 4.
- Single-take refs hold attention with other changes (caption pops, punch-ins, a cutaway card) and not with cuts.
- **CyberBrief target:** visible change every **~3–4 s** (a cut, punch-in or B-roll swap), with true cuts every ~5–8 s. Speech-to-speech jump cuts that remove breaths and retakes are expected.
- Dead air: none in any ref. Trim silence longer than ~0.25 s.

### Punch-in zooms
- Estimated from keyframes (head height changes between consecutive frames, and sub-threshold scene spikes in ref 4 at ~1.7, 2.6, 6.3, 16.4, 17.4, 30.2 and 40.6 s): **a punch-in every ~3–6 s**, **~1.10–1.20× scale**, held until the next one. Zooms alternate between "in" and "back to 1.0×".
- Zoom hits land on stressed words or the first word of a new sentence.
- CyberBrief: `every_seconds` 4, `scale` 1.12. Crop from a 4K or 1080p source so a 1.12× crop stays sharp.

### Framing
- Selfie, vertical, eye level or a little above, handheld arm's length or tripod. Medium close-up, shoulders visible.
- **Eyes at ~28–35% from the top of the frame**, head ~40–45% of the frame height, looking directly into the lens in every ref.
- Backgrounds are real places: car interior, balcony, outdoors, living room. All are bright and slightly out of focus, with no clutter. Natural daylight is the light source in all 9 refs.
- Leave the top ~15% free for the hook card and the bottom ~20% for captions or screenshot cards.

### Captions
- **Two styles are used.** (A) Word-level pops, **1–3 words per card**, UPPERCASE, bold sans, white with ONE highlight word in yellow (or red/pink), at ~75–82% down the frame (refs 3, 4, 5, 7, 9). (B) Phrase cards, **5–8 words**, lowercase, on yellow or white rounded boxes or white-with-outline at the top third (refs 6, 8, 10).
- Word-level pops match the channel's `word_level_burned_in` setting and read best at the fast WPM seen here (160–225).
- Emphasis: one highlighted word per card, chosen for the key noun or number. Numbers and "NO / FREE / COOL" style stress words are highlighted most often.
- CyberBrief default: style A, 3 words per card, UPPERCASE, white `#FFFFFF` with `#FFD400` highlight, 78% down, heavy black outline, weight 800.
- Section labels (list items, step numbers) use a separate pill at the top, such as "#3 NAME" or "STEP 2".

### Screen demos and B-roll
- Refs 5–10 use screens constantly. Refs 3 and 7–9 introduce them with a **hard cut or slide-in at the moment the speaker names the thing**, and they last 2–5 s each.
- Ref 7: one screen per list item (~5 s cadence). Ref 9: screen or generated output on nearly every item (every ~2–3 s).
- Two formats: **full-screen** (face disappears, voice continues, 2–3 s) and **picture-in-picture** (face shrinks to a bubble at the bottom corner, ~30–40% of frame width, for longer demos of 8+ s).
- Screens are phone or web screenshots of the real tool, or screenshots of posts as proof. Typing and the streaming answer are shown when it helps.
- CyberBrief: B-roll or screen every **~5 s** in a tip video, and ~35% of runtime on screen. Use real public pages first, then synthetic mock screens for scams (see `channel.yaml` `creator.visuals`).

### Sound
- Voice is loud and clean. A clip-on lav mic is visible in several refs. Music is **not audible or barely audible** in the analyzed refs, so I could not measure a level.
- No whooshes or SFX on cuts were detected in the audio energy data. This is not verified by ear.
- CyberBrief default (best-practice, not measured): a quiet bed at about **-24 dB** below the voice, ducked further during speech. A very light tick or whoosh on screen-swap cuts is optional (set `sfx_on_cuts` false until tested).

### Length and structure
- Measured lengths: 15, 25, 61, 61, 68, 83, 91, 113, 139 s. The list and how-to formats cluster at **60–90 s**.
- Structure seen across refs: **hook (0–3 s) → promise or context (3–10 s) → body in equal blocks (steps or items, ~5–12 s each) → payoff or takeaway → CTA**.
- CyberBrief: **45–70 s** (anything over 60 s also qualifies for TikTok Creator Rewards).

### CTA style
- Used: "save this video" and "follow" (asked early, within the first 15 s, in 2 of 9 refs), "link at the end" with a link-list screenshot (2 refs), and a profile page held on screen as a silent CTA (1 ref). Most CTAs are short, one sentence, and not a separate outro.
- CyberBrief: ask for a **save** early (after the promise, ~10 s) because tips are worth keeping. Close with the channel's follow line in under 4 s and a short "what to do now" before it.

---

## 3. Filming checklist for the owner (30-minute weekly batch for 5 scripts)

**Setup (5 min, once)**
- Phone vertical, rear camera if possible (the front camera is lower quality), 4K 30 fps (or 1080p 30 fps). Turn on Do Not Disturb. Lens wiped.
- Tripod or a stack of books so the phone is at eye level or slightly above. Camera at an arm's-length distance: head and shoulders visible with a little air above the hair.
- Look at the lens and not at your own face on the screen. Put a small sticker next to the lens.
- Light: face a window with daylight, or stand outside. Never put the window behind you. A cloudy day is fine.
- Background: one real place, tidy, a metre or two behind you. Film all five in the same spot, and change a top or a prop between scripts if you want variety.
- Audio: a clip-on lav mic (a wired one for the phone is fine). Quiet room, fridge and fans off. Record a 5 s test and listen with headphones.
- Teleprompter app on a second device or on the phone with a mirror rig, set to a pace of **~170–185 WPM**. The references run 160–225 WPM, so don't read slower than ~160.

**Per script (about 4–5 min each, 5 scripts)**
- Record **2 full takes** and stop. Don't aim for perfection, because the edit removes pauses and mistakes.
- Hook line: do it **3 times in a row** at the start of the take with a clap or a 1 s pause between them, so the best one can be picked.
- If you flub a line, pause for 2 s, say the line again from the start of that sentence, and carry on. Don't restart the whole take.
- Say stressed words with a slight lean toward the camera. Use one hand gesture per point (pointing, counting on fingers). These give the editor natural punch-in moments.
- No "um" fillers, and never stop at the end of a take before the CTA is finished.
- Say what is on screen aloud when you want a screen demo ("on the settings page…"), and pause for ~1 s. The editor places the screen there.
- Don't read out URLs, passwords or any real personal data. Do not show real accounts, and do not visit scam sites.

**Wrap-up (2 min)**
- Check the audio in the first and last take. Look at one frame for focus and exposure.
- Send each clip as a **reply to its script message in Telegram**, or name the file with the script id (`W44-1-take1.mp4`, …) when sending from the Mac or the Drive inbox.

---

## 4. Script template (≈55–60 s, ~165–195 spoken words)

Word counts assume ~180 WPM. Each beat is one or two short sentences, in plain English, for everyday people.

| Beat | Time | Words | What it does | On screen |
|---|---|---|---|---|
| 1. Hook | 0–3 s | 8–14 | The stakes or the payoff in the first sentence. A number, a "you're at risk" statement, or a "this tool does X" claim. Pay it off, never bait. | Hook card (4–7 words, top), caption pops from word 1 |
| 2. Why it matters | 3–9 s | 15–25 | Who it affects and what could go wrong or be gained, in one concrete example. Optional "save this" ask. | Punch-in, caption pops, optional pill "SAVE THIS" |
| 3. Step or point 1 | 9–19 s | 25–35 | One action, in one sentence, plus a five-word explanation of any jargon. | Screen or B-roll at the moment the thing is named, with a label pill |
| 4. Step or point 2 | 19–29 s | 25–35 | Same pattern. | Screen, PiP face |
| 5. Step or point 3 | 29–39 s | 25–35 | Same pattern. A tip video may have just 2 steps, with a longer step 3 or a "mistake to avoid". | Screen |
| 6. Payoff | 39–50 s | 20–30 | The result: what the viewer is now protected from or able to do. A single "do this today" action. | Face full-frame, punch-in on the action word |
| 7. CTA | 50–58 s | 10–15 | Follow line in the persona's voice, one sentence. | Follow text card or channel handle |

Rules for every script:
- Open with the claim, not with a greeting or the topic name.
- One idea per sentence, ≤14 words each. Read aloud, so no parentheses, and write numbers the way they are said.
- Defensive framing only. Facts come only from cited sources. End with what the viewer should do, as `channel.yaml` requires.
- Mark each step with a `[SCREEN: what to show]` tag so the edit agent can place a recording or mock screen.
- Mark one stress word per sentence in **bold** to drive the caption highlight and a punch-in.
- AI-tool videos: show the real public page of the tool, then say the one thing it does for you. Cyber-tip videos: show the threat on a synthetic screen, then the fix on a real settings page.

---

## 5. Limits of this study
- Ref 1 was not analyzed (816 s, over the 600 s cap).
- Zoom scale, caption colours and sizes are estimated from keyframes. Cut and WPM numbers are measured.
- Music level and SFX could not be measured reliably, so the defaults in `style.json` are best-practice values, not measurements.
- Both creators work in AI news and tutorials, so there are no cybersecurity-specific references, and the fast "list" format may fit tips less than step formats do.
