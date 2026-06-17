# WorldCup Insider 2026 — AI Social-Media Actor (real models)

A FIFA World Cup 2026 AI influencer built with **real AI models**. It takes the
**football photos you provide** and turns each one into a social-media post.

Link github: https://github.com/tktran05/ex3

| Module | Real model / tool | File |
|--------|-------------------|------|
| **1 · Computer Vision** | **YOLOv8** (ultralytics) — player/ball/crowd detection + jersey-colour recognition → spec JSON | `module1_vision.py` |
| **2 · Image Captioning** | **BLIP** (HuggingFace transformers) | `module2_caption.py` |
| **3 · Text Generation** | **Google Gemini** (persona-driven) | `module3_text.py` |
| **4 · Visual Content** | **Pillow** compositing the AI caption onto your real photo | `module4_visuals.py` |
| **Advanced** | Follower **memory database** (JSON) | `memory_db.py` |
| **Stage 3 UI** | Streamlit page: timeline, interactions, analytics | `app_streamlit.py` |

Pipeline: `your photo → YOLO → BLIP → Gemini → caption bar (Pillow) → posts.json → Streamlit page`.

---

## 1. Setup (Windows + NVIDIA GPU / CUDA)

```powershell
cd ai
# PyTorch with CUDA — install FIRST
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

Add your Gemini key (free at https://aistudio.google.com/apikey):

```powershell
copy .env.example .env
# edit .env -> GEMINI_API_KEY=...   (model gemini-2.5-flash)
```

> Without a key, Module 3 falls back to persona-consistent templates, so nothing breaks.
> YOLO + BLIP always run for real on the GPU.

---

## 2. Add your images
Drop FIFA World Cup photos into the typed folders (any number, `.jpg/.png/.webp`):

```
images/match/     images/player/     images/stadium/     images/team/     images/fan/
```

Each photo becomes one post that **displays that real image**. Empty folders are skipped.

---

## 3. Generate the posts

```powershell
python generate_posts.py            # one post per image + required Preview/Fan posts
python generate_posts.py --no-extra # only posts made from your images
```

Outputs:
- `output/posts.json` — all posts (caption, hashtags, CV JSON, image path)
- `output/posts/*.png` — your photos with the AI caption bar
- `output/image_analysis_report.json` — **Stage-1 deliverable** (caption + CV JSON per image)

> **6 GB VRAM note:** models load one at a time (YOLO → freed → BLIP → freed), fp16, so it fits an RTX 3060 Laptop.

---

## 4. Launch the page (Stage 3)

```powershell
streamlit run app_streamlit.py
```

Tabs: **Timeline · Analytics · Image Report · Memory DB**.
Like posts, vote in polls, answer quizzes, and **comment** — the actor replies with a
**personalised** message (Gemini + memory) and remembers your favourite team.

---

## Requirement coverage
- ✅ 5 post types: Match Summary (from your match photos), Player Spotlight, Stadium, Match Preview, Fan Community (poll/quiz/prediction)
- ✅ Posts built from your real images; ≥ 20 with the extra required types
- ✅ Image types processed: match, player, stadium, team, fan (+ collage)
- ✅ Modules 1–3 use the named real models; CV JSON matches `{players, ball, celebration, team}`
- ✅ Consistent persona (`persona.py`): enthusiastic/friendly/knowledgeable, fans 18–35
- ✅ Advanced memory DB + personalised replies
- ✅ Research extension: multimodal narrative ("Highlight Reel") from a sequence of your match photos
- ✅ Stage 3: timeline, publishing, follower interactions, analytics dashboard

## Responsible AI
Posts are clearly labelled **AI-generated**; results/stats are **illustrative**.
Follower memory is stored only locally in `output/memory.json` (git-ignored).
