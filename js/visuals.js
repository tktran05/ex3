/* =============================================================
   MODULE 4 — Visual Content Generator (Canvas == Pillow/OpenCV role)
   -------------------------------------------------------------
   Generates banners, posters, player thumbnails, stadium cards,
   collages and 1080×1920 story images entirely in the browser.
   Returns a data-URL (PNG) so posts can embed a real generated image
   without any external asset or AI image API.
   ============================================================= */

const Visuals = {
  _canvas(w, h) {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    return c;
  },

  _gradient(ctx, w, h, c1, c2, angle = "v") {
    const g = angle === "v"
      ? ctx.createLinearGradient(0, 0, 0, h)
      : ctx.createLinearGradient(0, 0, w, 0);
    g.addColorStop(0, c1);
    g.addColorStop(1, c2);
    return g;
  },

  _shade(hex, amt) {
    const n = parseInt(hex.slice(1), 16);
    let r = (n >> 16) + amt, g = ((n >> 8) & 255) + amt, b = (n & 255) + amt;
    r = Math.max(0, Math.min(255, r)); g = Math.max(0, Math.min(255, g)); b = Math.max(0, Math.min(255, b));
    return `rgb(${r},${g},${b})`;
  },

  _watermark(ctx, w, h) {
    ctx.font = "bold 20px Inter, Arial";
    ctx.fillStyle = "rgba(255,255,255,0.85)";
    ctx.textAlign = "right";
    ctx.fillText("🌍 WorldCup Insider 2026", w - 24, h - 22);
    ctx.textAlign = "left";
  },

  _wrap(ctx, text, x, y, maxW, lh) {
    const words = text.split(" ");
    let line = "";
    for (const word of words) {
      const test = line + word + " ";
      if (ctx.measureText(test).width > maxW && line) {
        ctx.fillText(line.trim(), x, y);
        line = word + " ";
        y += lh;
      } else line = test;
    }
    ctx.fillText(line.trim(), x, y);
    return y;
  },

  /* -------- Match preview / summary banner (1200×630) -------- */
  matchBanner(home, away, opts = {}) {
    const w = 1200, h = 630;
    const c = this._canvas(w, h), ctx = c.getContext("2d");
    const hc = teamColor(home, 0), ac = teamColor(away, 0);

    // split background
    ctx.fillStyle = this._shade(hc, -30);
    ctx.fillRect(0, 0, w / 2, h);
    ctx.fillStyle = this._shade(ac, -30);
    ctx.fillRect(w / 2, 0, w / 2, h);
    // diagonal seam
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.beginPath();
    ctx.moveTo(w / 2 - 60, 0); ctx.lineTo(w / 2 + 60, 0);
    ctx.lineTo(w / 2 - 60, h); ctx.lineTo(w / 2 - 180, h);
    ctx.closePath(); ctx.fill();

    // flags
    ctx.font = "150px Arial";
    ctx.textAlign = "center";
    ctx.fillText(teamFlag(home), w * 0.25, h * 0.45);
    ctx.fillText(teamFlag(away), w * 0.75, h * 0.45);

    // VS
    ctx.fillStyle = "#fff";
    ctx.font = "bold 72px Inter, Arial";
    ctx.fillText("VS", w / 2, h * 0.42);

    // names
    ctx.font = "bold 46px Inter, Arial";
    ctx.fillText(home.toUpperCase(), w * 0.25, h * 0.62);
    ctx.fillText(away.toUpperCase(), w * 0.75, h * 0.62);

    // banner strip
    ctx.fillStyle = "rgba(0,0,0,0.55)";
    ctx.fillRect(0, h * 0.74, w, h * 0.18);
    ctx.fillStyle = "#FFD700";
    ctx.font = "bold 34px Inter, Arial";
    ctx.fillText(opts.label || "FIFA WORLD CUP 2026", w / 2, h * 0.83);
    if (opts.sub) {
      ctx.fillStyle = "#fff";
      ctx.font = "26px Inter, Arial";
      ctx.fillText(opts.sub, w / 2, h * 0.885);
    }
    ctx.textAlign = "left";
    this._watermark(ctx, w, h);
    return c.toDataURL("image/png");
  },

  /* -------- Player spotlight thumbnail (800×800) -------- */
  playerThumb(p) {
    const w = 800, h = 800;
    const c = this._canvas(w, h), ctx = c.getContext("2d");
    const col = teamColor(p.team, 0);
    ctx.fillStyle = this._gradient(ctx, w, h, this._shade(col, 20), this._shade(col, -60));
    ctx.fillRect(0, 0, w, h);

    // big number
    ctx.fillStyle = "rgba(255,255,255,0.10)";
    ctx.font = "bold 520px Inter, Arial";
    ctx.textAlign = "center";
    ctx.fillText(p.number, w / 2, h * 0.78);

    // flag
    ctx.font = "180px Arial";
    ctx.fillText(teamFlag(p.team), w / 2, h * 0.42);

    // name
    ctx.fillStyle = "#fff";
    ctx.font = "bold 56px Inter, Arial";
    ctx.fillText(p.name.toUpperCase(), w / 2, h * 0.6);
    ctx.font = "30px Inter, Arial";
    ctx.fillStyle = "#FFD700";
    ctx.fillText(`${p.pos} · ${p.team}`, w / 2, h * 0.66);

    // stat strip
    ctx.fillStyle = "rgba(0,0,0,0.45)";
    ctx.fillRect(0, h * 0.82, w, h * 0.18);
    ctx.fillStyle = "#fff";
    ctx.font = "bold 30px Inter, Arial";
    ctx.fillText(`${p.stats.caps} CAPS   ·   ${p.stats.goals} GOALS   ·   ${p.stats.assists} ASSISTS`, w / 2, h * 0.915);
    ctx.textAlign = "left";
    this._watermark(ctx, w, h);
    return c.toDataURL("image/png");
  },

  /* -------- Stadium travel card (1200×630) -------- */
  stadiumCard(s) {
    const w = 1200, h = 630;
    const c = this._canvas(w, h), ctx = c.getContext("2d");
    ctx.fillStyle = this._gradient(ctx, w, h, "#0b3d2e", "#072019");
    ctx.fillRect(0, 0, w, h);

    // skyline-ish bars
    ctx.fillStyle = "rgba(255,255,255,0.06)";
    for (let i = 0; i < 14; i++) {
      const bw = 70, bh = 120 + Math.random() * 220;
      ctx.fillRect(i * bw, h - bh, bw - 8, bh);
    }
    ctx.font = "120px Arial"; ctx.textAlign = "center";
    ctx.fillText("🏟️", w / 2, h * 0.4);

    ctx.fillStyle = "#fff";
    ctx.font = "bold 50px Inter, Arial";
    ctx.fillText(s.name, w / 2, h * 0.58);
    ctx.font = "30px Inter, Arial";
    ctx.fillStyle = "#7CFFB2";
    ctx.fillText(`📍 ${s.city}, ${s.country}   ·   👥 ${s.capacity.toLocaleString()}`, w / 2, h * 0.66);

    ctx.fillStyle = "rgba(0,0,0,0.5)";
    ctx.fillRect(0, h * 0.78, w, h * 0.22);
    ctx.fillStyle = "#FFD700";
    ctx.font = "bold 26px Inter, Arial";
    ctx.fillText("HOST VENUE · FIFA WORLD CUP 2026", w / 2, h * 0.88);
    ctx.textAlign = "left";
    this._watermark(ctx, w, h);
    return c.toDataURL("image/png");
  },

  /* -------- Generic poll/quiz/prediction card (1080×1080) -------- */
  promptCard(title, lines, theme = "#5b21b6") {
    const w = 1080, h = 1080;
    const c = this._canvas(w, h), ctx = c.getContext("2d");
    ctx.fillStyle = this._gradient(ctx, w, h, this._shade(theme, 30), this._shade(theme, -50));
    ctx.fillRect(0, 0, w, h);
    ctx.textAlign = "center";
    ctx.font = "120px Arial";
    ctx.fillText("📊", w / 2, h * 0.2);
    ctx.fillStyle = "#fff";
    ctx.font = "bold 60px Inter, Arial";
    this._wrap(ctx, title, w / 2, h * 0.32, w * 0.8, 70);

    ctx.font = "bold 44px Inter, Arial";
    let y = h * 0.5;
    lines.forEach(l => {
      ctx.fillStyle = "rgba(255,255,255,0.14)";
      ctx.fillRect(w * 0.12, y - 48, w * 0.76, 72);
      ctx.fillStyle = "#fff";
      ctx.fillText(l, w / 2, y);
      y += 105;
    });
    ctx.textAlign = "left";
    this._watermark(ctx, w, h);
    return c.toDataURL("image/png");
  },

  /* -------- Collage of "top moments" (1200×800, 2×2) -------- */
  collage(items) {
    const w = 1200, h = 800;
    const c = this._canvas(w, h), ctx = c.getContext("2d");
    ctx.fillStyle = "#0d0d0d"; ctx.fillRect(0, 0, w, h);
    const cells = [[0, 0], [w / 2, 0], [0, h / 2], [w / 2, h / 2]];
    items.slice(0, 4).forEach((it, i) => {
      const [x, y] = cells[i];
      ctx.fillStyle = this._gradient(ctx, w, h, this._shade(it.color, 10), this._shade(it.color, -60));
      ctx.fillRect(x + 6, y + 6, w / 2 - 12, h / 2 - 12);
      ctx.textAlign = "center";
      ctx.font = "90px Arial";
      ctx.fillText(it.emoji, x + w / 4, y + h / 4);
      ctx.fillStyle = "#fff";
      ctx.font = "bold 30px Inter, Arial";
      ctx.fillText(it.label, x + w / 4, y + h / 4 + 90);
    });
    ctx.fillStyle = "#FFD700";
    ctx.textAlign = "center";
    ctx.font = "bold 34px Inter, Arial";
    ctx.fillText("TOP MOMENTS · WORLD CUP 2026", w / 2, h / 2 + 8);
    ctx.textAlign = "left";
    return c.toDataURL("image/png");
  },

  /* -------- 1080×1920 story image -------- */
  story(title, subtitle, theme = "#1a73e8") {
    const w = 1080, h = 1920;
    const c = this._canvas(w, h), ctx = c.getContext("2d");
    ctx.fillStyle = this._gradient(ctx, w, h, this._shade(theme, 30), this._shade(theme, -70));
    ctx.fillRect(0, 0, w, h);
    ctx.textAlign = "center";
    ctx.font = "200px Arial";
    ctx.fillText("⚽", w / 2, h * 0.32);
    ctx.fillStyle = "#fff";
    ctx.font = "bold 78px Inter, Arial";
    this._wrap(ctx, title, w / 2, h * 0.5, w * 0.84, 92);
    ctx.font = "40px Inter, Arial";
    ctx.fillStyle = "rgba(255,255,255,0.85)";
    this._wrap(ctx, subtitle, w / 2, h * 0.66, w * 0.8, 56);
    ctx.fillStyle = "#FFD700";
    ctx.font = "bold 36px Inter, Arial";
    ctx.fillText("🌍 WorldCup Insider 2026", w / 2, h * 0.92);
    ctx.textAlign = "left";
    return c.toDataURL("image/png");
  }
};
