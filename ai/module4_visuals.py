"""
MODULE 4 — Visual Content Generator  (Stable Diffusion + Pillow/OpenCV)
----------------------------------------------------------------------
Generates the banner / poster / thumbnail / collage / story images.
- Stable Diffusion (diffusers) paints a football background from a text prompt.
- Pillow composites the headline, names, score, logo and a footer onto it.
- If SD is disabled or fails, a clean gradient background is used instead so
  the pipeline always produces a real image.

Note: Pillow cannot render colour emoji, so poster text uses plain text/shapes;
emojis live in the post *caption* (rendered by the UI).
"""
from __future__ import annotations
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import config
from data import team_color

_FONT_CANDIDATES = ["segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
_FONT_REG = ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]


def _font(size, bold=True):
    for name in (_FONT_CANDIDATES if bold else _FONT_REG):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _shade(rgb, amt):
    return tuple(max(0, min(255, c + amt)) for c in rgb)


def _ascii(s):
    """Drop emoji / non-Latin glyphs Pillow can't render, for text drawn on images."""
    import re
    s = re.sub(r"[^\x20-\x7E -ɏ]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _gradient(size, c1, c2, vertical=True):
    w, h = size
    try:
        import numpy as np
        t = (np.linspace(0, 1, h)[:, None] if vertical else np.linspace(0, 1, w)[None, :])
        t = np.broadcast_to(t, (h, w))[..., None]
        c1a, c2a = np.array(c1, float), np.array(c2, float)
        arr = (c1a * (1 - t) + c2a * t).astype("uint8")
        return Image.fromarray(arr, "RGB")
    except Exception:
        base = Image.new("RGB", size, c1)
        top = Image.new("RGB", size, c2)
        mask = Image.new("L", size)
        md = mask.load()
        for y in range(h):
            for x in range(w):
                md[x, y] = int(255 * (y / h if vertical else x / w))
        base.paste(top, (0, 0), mask)
        return base


def _draw_center(draw, text, font, cx, y, fill="white"):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def _wrap_center(draw, text, font, cx, y, max_chars, lh, fill="white"):
    for line in textwrap.wrap(text, max_chars):
        _draw_center(draw, line, font, cx, y, fill)
        y += lh
    return y


class VisualGenerator:
    def __init__(self, use_sd: bool | None = None):
        self.use_sd = config.USE_STABLE_DIFFUSION if use_sd is None else use_sd
        self._pipe = None

    # ---- Stable Diffusion (lazy) -------------------------------------
    def _sd(self):
        if self._pipe is not None:
            return self._pipe
        if not self.use_sd:
            return None
        try:
            import torch
            from diffusers import AutoPipelineForText2Image
            pipe = AutoPipelineForText2Image.from_pretrained(
                config.SD_MODEL,
                torch_dtype=torch.float16 if config.DEVICE == "cuda" else torch.float32,
            )
            pipe = pipe.to(config.DEVICE)
            pipe.set_progress_bar_config(disable=True)
            try:
                pipe.enable_attention_slicing()
                pipe.enable_vae_slicing()
            except Exception:
                pass
            self._pipe = pipe
        except Exception as e:
            print(f"[SD] disabled ({e}); using gradient backgrounds.")
            self.use_sd = False
            self._pipe = None
        return self._pipe

    def _background(self, prompt, size, fallback_colors):
        pipe = self._sd()
        if pipe is not None:
            try:
                steps = 2 if "turbo" in config.SD_MODEL else 25
                guidance = 0.0 if "turbo" in config.SD_MODEL else 7.5
                img = pipe(prompt=prompt, num_inference_steps=steps,
                           guidance_scale=guidance, height=512, width=512).images[0]
                return img.resize(size).filter(ImageFilter.GaussianBlur(0.4))
            except Exception as e:
                print(f"[SD] generation failed ({e}); gradient fallback.")
        return _gradient(size, _shade(fallback_colors[0], -30),
                         _shade(fallback_colors[-1], -70))

    def free(self):
        if self._pipe is not None:
            try:
                import torch
                del self._pipe
                self._pipe = None
                torch.cuda.empty_cache()
            except Exception:
                pass

    # ---- footer watermark --------------------------------------------
    @staticmethod
    def _footer(img):
        d = ImageDraw.Draw(img)
        w, h = img.size
        d.rectangle([0, h - 46, w, h], fill=(0, 0, 0))
        d.text((20, h - 38), "WorldCup Insider 2026", font=_font(22), fill=(255, 215, 0))
        return img

    def _save(self, img, name):
        path = config.POSTS_DIR / name
        img.save(path, "PNG")
        return str(path)

    # ---- Compose the AI text onto the USER'S real photo --------------
    def compose_on_photo(self, image_path, category, headline, name, width=1080):
        """Use the user's real image as the post visual, with a clean badge
        (top) and a translucent caption bar + watermark (bottom)."""
        try:
            photo = Image.open(image_path).convert("RGB")
        except Exception:
            # if the photo can't be opened, fall back to a gradient card
            photo = _gradient((width, int(width * 0.66)), (20, 40, 80), (8, 16, 32))
        # scale to a consistent width, cap very tall images
        w = width
        h = max(1, int(photo.height * w / photo.width))
        h = min(h, int(width * 1.5))
        photo = photo.resize((w, h))

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        # top category badge
        bf = _font(30)
        bb = d.textbbox((0, 0), category, font=bf)
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        d.rounded_rectangle([24, 24, 24 + bw + 36, 24 + bh + 28], radius=16, fill=(26, 115, 232, 230))
        d.text((42, 36), category, font=bf, fill=(255, 255, 255, 255))

        # bottom caption bar (strip emoji Pillow can't draw)
        lines = textwrap.wrap(_ascii(headline), 42)[:3] or [category]
        bar_h = 56 + len(lines) * 46 + 44
        d.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 170))
        y = h - bar_h + 22
        for ln in lines:
            d.text((30, y), ln, font=_font(34), fill=(255, 255, 255, 255))
            y += 46
        d.text((30, h - 40), "WorldCup Insider 2026", font=_font(24), fill=(255, 215, 0, 255))

        out = Image.alpha_composite(photo.convert("RGBA"), overlay).convert("RGB")
        return self._save(out, name)

    # ================= GENERATORS =================

    def match_banner(self, home, away, label, name):
        w, h = 1200, 630
        prompt = (f"epic football stadium, world cup 2026, dramatic lighting, "
                  f"{home} vs {away}, cinematic, crowd, no text")
        img = self._background(prompt, (w, h), [team_color(home), team_color(away)]).convert("RGB")
        # dark overlay for legibility
        ov = Image.new("RGB", (w, h), (0, 0, 0))
        img = Image.blend(img, ov, 0.35)
        d = ImageDraw.Draw(img)
        # team colour side bars
        d.rectangle([0, 0, 16, h], fill=team_color(home))
        d.rectangle([w - 16, 0, w, h], fill=team_color(away))
        _draw_center(d, f"{home.upper()}  VS  {away.upper()}", _font(60), w / 2, h * 0.30)
        d.rectangle([0, int(h * 0.62), w, int(h * 0.78)], fill=(0, 0, 0))
        _draw_center(d, label, _font(34), w / 2, h * 0.655, fill=(255, 215, 0))
        self._footer(img)
        return self._save(img, name)

    def player_thumb(self, p, name):
        w, h = 800, 800
        col = team_color(p["team"])
        prompt = f"professional football player portrait, {p['team']} jersey, stadium bokeh, no text"
        img = self._background(prompt, (w, h), [col]).convert("RGB")
        img = Image.blend(img, Image.new("RGB", (w, h), (0, 0, 0)), 0.30)
        d = ImageDraw.Draw(img)
        # big number watermark
        d.text((w * 0.62, h * 0.05), f"#{p['number']}", font=_font(160), fill=(255, 255, 255, 40))
        d.rectangle([0, int(h * 0.66), w, int(h * 0.84)], fill=(0, 0, 0))
        _draw_center(d, p["name"].upper(), _font(46), w / 2, h * 0.55)
        _draw_center(d, f"{p['pos']} · {p['team']}", _font(28), w / 2, h * 0.69, fill=(255, 215, 0))
        s = p["stats"]
        _draw_center(d, f"{s['caps']} CAPS   {s['goals']} GOALS   {s['assists']} ASSISTS",
                     _font(26), w / 2, h * 0.755)
        self._footer(img)
        return self._save(img, name)

    def stadium_card(self, s, name):
        w, h = 1200, 630
        prompt = f"{s['name']} football stadium exterior, {s['city']}, sunset, wide shot, no text"
        img = self._background(prompt, (w, h), [(11, 61, 46), (7, 32, 25)]).convert("RGB")
        img = Image.blend(img, Image.new("RGB", (w, h), (0, 0, 0)), 0.30)
        d = ImageDraw.Draw(img)
        _draw_center(d, s["name"], _font(54), w / 2, h * 0.55)
        _draw_center(d, f"{s['city']}, {s['country']}  -  {s['capacity']:,} seats",
                     _font(30), w / 2, h * 0.68, fill=(124, 255, 178))
        d.rectangle([0, int(h * 0.80), w, int(h * 0.90)], fill=(0, 0, 0))
        _draw_center(d, "HOST VENUE - FIFA WORLD CUP 2026", _font(26), w / 2, h * 0.825, fill=(255, 215, 0))
        self._footer(img)
        return self._save(img, name)

    def prompt_card(self, title, lines, name, theme=(91, 33, 182)):
        w, h = 1080, 1080
        img = _gradient((w, h), _shade(theme, 30), _shade(theme, -50))
        d = ImageDraw.Draw(img)
        _wrap_center(d, title, _font(58), w / 2, h * 0.18, 22, 70)
        y = int(h * 0.42)
        for ln in lines:
            d.rounded_rectangle([w * 0.12, y, w * 0.88, y + 84], radius=18, fill=(255, 255, 255, 30))
            _draw_center(d, ln, _font(40), w / 2, y + 22)
            y += 110
        self._footer(img)
        return self._save(img, name)

    def collage(self, image_paths, name, title="TOP MOMENTS - WORLD CUP 2026"):
        w, h = 1200, 800
        canvas = Image.new("RGB", (w, h), (13, 13, 13))
        cells = [(0, 0), (w // 2, 0), (0, h // 2), (w // 2, h // 2)]
        cw, ch = w // 2 - 8, h // 2 - 8
        for (x, y), p in zip(cells, image_paths[:4]):
            try:
                tile = Image.open(p).convert("RGB").resize((cw, ch))
            except Exception:
                tile = _gradient((cw, ch), (30, 60, 120), (10, 20, 40))
            canvas.paste(tile, (x + 4, y + 4))
        d = ImageDraw.Draw(canvas)
        d.rectangle([0, h // 2 - 30, w, h // 2 + 30], fill=(0, 0, 0))
        _draw_center(d, title, _font(34), w / 2, h // 2 - 22, fill=(255, 215, 0))
        return self._save(canvas, name)

    def story(self, title, subtitle, name, theme=(26, 115, 232)):
        w, h = 1080, 1920
        img = _gradient((w, h), _shade(theme, 30), _shade(theme, -70))
        d = ImageDraw.Draw(img)
        _wrap_center(d, title, _font(78), w / 2, h * 0.40, 18, 92)
        _wrap_center(d, subtitle, _font(40), w / 2, h * 0.60, 30, 56, fill=(230, 230, 230))
        _draw_center(d, "WorldCup Insider 2026", _font(40), w / 2, h * 0.90, fill=(255, 215, 0))
        return self._save(img, name)
