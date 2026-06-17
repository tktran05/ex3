"""
ORCHESTRATOR — build the AI actor's content set FROM YOUR REAL IMAGES.

Each image you drop in images/<type>/ becomes one post that DISPLAYS that
real photo, analysed by real models:

    your photo -> [YOLO] -> [BLIP] -> [Gemini] -> caption bar (Pillow) -> post

Required text-only post types (Match Preview, Fan poll/quiz/prediction) are
added on top so all 5 brief categories and the 20-post minimum are covered.

To stay within 6 GB VRAM the heavy models run ONE at a time (YOLO, then BLIP;
Gemini is an API call; Stable Diffusion is not needed here).

Usage:
    python generate_posts.py
    python generate_posts.py --no-extra     # only posts made from your images
"""
from __future__ import annotations
import argparse
import json
import random
import re
from pathlib import Path

import config
from data import FIXTURES, GROUPS, PLAYERS, PLAYER_BY_NAME, team_flag
from module3_text import TextGenerator
from module4_visuals import VisualGenerator

CATEGORY = {
    "match": "Match Summary", "player": "Player Spotlight",
    "stadium": "Stadium", "team": "Team", "fan": "Fan Community",
}
ICON = {"match": "📸", "player": "🌟", "stadium": "🏟️", "team": "📷", "fan": "🎉"}

ALIASES = {
    "ronaldo": "Cristiano Ronaldo", "rolnado": "Cristiano Ronaldo", "messi": "Lionel Messi",
    "mbappe": "Kylian Mbappe", "bellingham": "Jude Bellingham", "vinicius": "Vinicius Junior",
    "kane": "Harry Kane", "yamal": "Lamine Yamal", "pulisic": "Christian Pulisic",
}


def free_cuda():
    try:
        import torch, gc
        gc.collect(); torch.cuda.empty_cache()
    except Exception:
        pass


def list_images(kind):
    folder = config.IMAGES_DIR / kind
    exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    return sorted(p for p in folder.glob("*") if p.suffix.lower() in exts)


def guess_player(filename: str):
    s = filename.lower()
    for k, v in ALIASES.items():
        if k in s:
            return PLAYER_BY_NAME.get(v), v
    for p in PLAYERS:
        if p["name"].lower().split()[-1] in s:
            return p, p["name"]
    words = [w for w in re.sub(r"[^a-z ]+", " ", s).split() if len(w) > 2]
    if 1 <= len(words) <= 3 and not re.search(r"\d{4,}", s):
        return None, " ".join(words).title()
    return None, "World Cup Star"


# ----------------------------------------------------------------------
# PHASE 1 + 2 — YOLO + BLIP on your real images (also = Stage-1 report)
# ----------------------------------------------------------------------
def analyze_images():
    all_imgs = {t: list_images(t) for t in config.IMAGE_TYPES}
    total = sum(len(v) for v in all_imgs.values())
    if total == 0:
        print("[!] No images found in images/<type>/. Add photos and re-run.")
        return [], []

    from module1_vision import VisionModule
    print(f"[1/3] Computer Vision (YOLO) on {total} images ...")
    vm = VisionModule()
    entries = []
    for kind, imgs in all_imgs.items():
        for p in imgs:
            det = vm.analyze(str(p), meta={} if kind == "team" else {"team": None})
            entries.append({"path": str(p), "kind": kind, "det": det, "caption": None})
            print(f"    {kind:8} {p.name[:40]:40} -> {VisionModule.to_spec_json(det)}")
    del vm; free_cuda()

    print(f"[2/3] Captioning (BLIP) on {total} images ...")
    from module2_caption import CaptionModule
    cm = CaptionModule()
    report = []
    for e in entries:
        e["caption"] = cm.caption(e["path"])
        report.append({"image": Path(e["path"]).name, "type": e["kind"],
                       "caption": e["caption"],
                       "vision_json": VisionModule.to_spec_json(e["det"])})
        print(f"    {Path(e['path']).name[:40]:40} -> {e['caption']}")
    del cm; free_cuda()

    config.REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"    -> {config.REPORT_JSON.name} ({len(report)} rows)")
    return entries, report


# ----------------------------------------------------------------------
# PHASE 3 — Gemini text + post built on the REAL photo
# ----------------------------------------------------------------------
def build_posts(entries, add_extra=True):
    from module1_vision import VisionModule
    print("[3/3] Text (Gemini) + composing posts on your real photos ...")
    tg = TextGenerator()
    print(f"    Gemini enabled: {tg.enabled} (model {config.GEMINI_MODEL})")
    vg = VisualGenerator(use_sd=False)   # use the real photos, no synthetic images

    posts, pid = [], [0]

    def add(**p):
        pid[0] += 1
        p["id"] = pid[0]
        p["likes"] = random.randint(120, 9800)
        p["comments"] = []
        posts.append(p)
        print(f"    + #{p['id']:>2} {p['category']}")

    # ---- one post per real image ----
    for e in entries:
        kind, vjson = e["kind"], VisionModule.to_spec_json(e["det"])
        hints = {}
        if kind == "player":
            db, nm = guess_player(Path(e["path"]).name)
            hints = {"name": nm, "db": db}
        t = tg.from_photo(kind, e["caption"], vjson, hints)
        headline = t["caption"].split("\n")[0][:120]
        img = vg.compose_on_photo(e["path"], CATEGORY[kind], headline, f"{kind}_{pid[0]+1}.png")
        add(category=CATEGORY[kind], icon=ICON[kind], image=img,
            caption=t["caption"], hashtags=t["hashtags"],
            vision=vjson, source_image=Path(e["path"]).name)

    if add_extra:
        # ---- Match Preview (required type; text + Pillow banner) ----
        for fx in FIXTURES[:3]:
            tt = tg.match_preview(fx)
            img = vg.match_banner(fx["home"], fx["away"],
                                  f"GROUP {fx['group']} - {fx['date']}", f"preview_{pid[0]+1}.png")
            add(category="Match Preview", icon="📅", image=img,
                caption=tt["caption"], hashtags=tt["hashtags"])

        # ---- Fan Community (required type): polls + quiz + prediction ----
        for g in ["D", "C"]:
            pl = tg.fan_poll(g)
            img = vg.prompt_card(f"Who wins Group {g}?",
                                 [f"{chr(65+i)}. {o}" for i, o in enumerate(pl["options"])],
                                 f"poll_{pid[0]+1}.png")
            add(category="Fan Community", icon="📊", kind="poll", image=img,
                caption=pl["caption"], hashtags=pl["hashtags"],
                poll={"options": pl["options"], "votes": [random.randint(50, 1200) for _ in pl["options"]]})
        q = tg.fan_quiz()
        img = vg.prompt_card("Quiz Time!", [f"{chr(65+i)}. {o}" for i, o in enumerate(q["options"])],
                             f"quiz_{pid[0]+1}.png", theme=(15, 118, 110))
        add(category="Fan Community", icon="🧠", kind="quiz", image=img,
            caption=q["caption"], hashtags=q["hashtags"],
            quiz={"answer": q["answer"], "options": q["options"]})
        pr = tg.fan_prediction()
        img = vg.story("Bold Prediction", "Who goes all the way in 2026?",
                       f"pred_{pid[0]+1}.png", theme=(185, 28, 28))
        add(category="Fan Community", icon="🔮", kind="prediction", image=img,
            caption=pr["caption"], hashtags=pr["hashtags"])

        # ---- Research extension: multimodal narrative from your match photos ----
        match_imgs = [e["path"] for e in entries if e["kind"] == "match"]
        if match_imgs:
            img = vg.collage(match_imgs, f"collage_{pid[0]+1}.png")
            add(category="Highlight Reel", icon="🎬", image=img,
                caption=("🎬 TOP MOMENTS!\n\nYour World Cup photos, stitched into one story. 🔥\n"
                         "Goals, battles and celebrations. Which is your favourite? 👇"),
                hashtags=["#TopMoments", "#Highlights", "#WorldCup2026", "#WeAre26"])

    vg.free(); free_cuda()
    return posts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-extra", action="store_true",
                    help="only build posts from your images (skip preview/fan/collage)")
    args = ap.parse_args()

    random.seed()
    entries, report = analyze_images()
    posts = build_posts(entries, add_extra=not args.no_extra)

    out = {
        "persona": __import__("persona").PERSONA,
        "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "report_rows": len(report),
        "posts": posts,
    }
    config.POSTS_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    from collections import Counter
    print(f"\n✅ {len(posts)} posts -> {config.POSTS_JSON}")
    print("   by type:", dict(Counter(p['category'] for p in posts)))
    print(f"   images  -> {config.POSTS_DIR}")
    print(f"   report  -> {config.REPORT_JSON} ({len(report)} rows)")


if __name__ == "__main__":
    main()
