# WorldCup Insider 2026 — AI Social-Media Actor

**Exercise 3 — Digital Content Programming**

This repository contains **two versions** of the project:

| Version | Folder | Tech |
|---------|--------|------|
| **A · Browser demo** (this README) | repo root (`index.html`) | Pure JavaScript — no install, runs anywhere |
| **B · Real AI models** ([see `ai/`](ai/README.md)) | `ai/` | YOLOv8 + BLIP + Google Gemini, on GPU |

---

## Version A — Browser demo
A self-contained, browser-based **simulated social network** running an AI influencer that
automatically analyses FIFA World Cup 2026 images and publishes multimedia posts.

> No server, no install, no GPU. Open `index.html` in any modern browser. Everything
> (computer vision, captioning, text generation, poster generation, analytics, follower
> memory) runs client-side in JavaScript.

---

## ▶️ How to run
Double-click **`index.html`** (or right-click → Open with browser).
Use the tabs: **Timeline · Analytics · Image Analysis Report · Memory DB**.
- **🔄 Generate new posts** — re-runs the whole AI pipeline with fresh random data.
- Like, comment, vote in polls, answer quizzes — the actor replies and remembers you.

---

## 🧠 Architecture (matches the brief's diagram)

```
FIFA Images  →  Image Processing Layer
                        │
        ┌───────────────┴───────────────┐
   Computer Vision                  Captioning
   (Module 1)                       (Module 2)
        └───────────────┬───────────────┘
                  LLM Content Engine (Module 3)
                        │
                  Visual Content Generator (Module 4)
                        │
                  Social Media Actor  →  Followers
```

| File | Role |
|------|------|
| `js/data.js`       | Knowledge base: 18 teams, star players, host stadiums, fixtures, groups |
| `js/vision.js`     | **Module 1 — Computer Vision** (simulated YOLO/Detectron2/Grounding DINO/Florence-2). Outputs the exact spec JSON `{players, ball, celebration, team}` |
| `js/captioning.js` | **Module 2 — Image Captioning** (simulated BLIP/BLIP-2/LLaVA) |
| `js/generator.js`  | **Module 3 — Text Generator** (simulated GPT/Llama/Gemma) + the `WorldCup Insider 2026` persona |
| `js/visuals.js`    | **Module 4 — Visual Content Generator** (Canvas = Pillow/OpenCV role): banners, thumbnails, stadium cards, collages, 1080×1920 stories |
| `js/memory.js`     | **Advanced Challenge** — per-follower memory DB (localStorage) |
| `js/app.js`        | Orchestration: builds 24 posts, renders feed, analytics, report, interactions |
| `index.html` / `css/styles.css` | The simulated social-network page |

---

## ✅ Requirement coverage

### Five required post types
1. **Match Preview** — generated banner + AI caption + hashtags.
2. **Match Summary** — runs CV→caption→text on a match photo; identifies teams/players/scoreboard/celebration and writes *"Argentina defeated Austria 2-1 in a dramatic encounter…"*.
3. **Player Spotlight** — profile, career stats, fun facts, generated thumbnail.
4. **Stadium** — venue, architecture, capacity, host city → travel-style post.
5. **Fan Community** — polls (*"Who will win Group D?"*), quizzes, predictions.

### Multimedia inputs processed
Team photos · Match photos · Player portraits · Stadium images · Fan photos · (collage) Infographics.

### Deliverables
- **Stage 1:** Image Analysis Report tab — captions + CV JSON for every source image.
- **Stage 2:** 24 auto-generated posts (≥ 20 required) with posters & hashtags.
- **Stage 3:** Working page timeline, automated publishing, follower interactions, analytics dashboard.

### Persona
`WorldCup Insider 2026` — Enthusiastic · Friendly · Knowledgeable · audience 18–35 · short sentences, emojis, high engagement.

### Advanced + Research extension
- **Memory DB:** remembers `{user, favorite_team, last_comment}` and personalises replies.
- **Multimodal narrative:** a "Visual Storytelling" post stitches a sequence of match images into one temporal story (*"Brazil dominated possession… scored in the second half… celebrated with thousands of fans."*).

---

## ⚖️ Responsible / Ethical AI
- Every post is clearly produced by an **AI Actor** (badge in header + footer disclaimer).
- Content is labelled **auto-generated for educational purposes**; players, results and stats are **illustrative**, not real predictions.
- No real personal data is collected — follower "memory" is stored only in the local browser.

---

## 🔁 Upgrading to real models (production notes)
Each simulated module exposes the same contract a real model would, so swapping is localised:
- `Vision.analyze()` → call a YOLOv8 / Florence-2 endpoint, return the same JSON.
- `Captioning.caption()` → call BLIP-2 / LLaVA.
- `Generator.*` → send `PERSONA.systemPrompt` + caption to a GPT/Llama/Gemma API.
- `Visuals.*` → replace Canvas with Stable Diffusion / Canva API output.
