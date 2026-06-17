/* =============================================================
   APP — Social Media Actor orchestration + feed + analytics
   Pipeline:  Image → Vision → Captioning → LLM Generator → Visuals → Post
   ============================================================= */

const Feed = {
  posts: [],
  reportRows: [],

  /* ---------- Build the multimedia "image library" inputs ---------- */
  buildImageLibrary() {
    const imgs = [];
    // match photos (from finished simulated results)
    WC2026.fixtures.forEach(fx => {
      const hs = randInt(0, 3), as_ = randInt(0, 3);
      imgs.push({
        type: "match", home: fx.home, away: fx.away, venue: fx.venue,
        winner: hs > as_ ? fx.home : as_ > hs ? fx.away : null,
        result: { hs, as_ }
      });
    });
    // team photos
    WC2026.teams.slice(0, 6).forEach(t => imgs.push({ type: "team", team: t.name }));
    // player portraits
    WC2026.players.forEach(p => imgs.push({ type: "player", team: p.team, player: p }));
    // stadium images
    WC2026.stadiums.forEach(s => imgs.push({ type: "stadium", stadium: s, team: null }));
    // fan photos
    ["Brazil", "Argentina", "Mexico", "England"].forEach(t => imgs.push({ type: "fan", team: t }));
    return imgs;
  },

  /* ---------- Generate the full set of posts ---------- */
  generateAll() {
    this.posts = [];
    this.reportRows = [];
    let id = 1;
    const add = (p) => { p.id = id++; p.likes = randInt(120, 9800); p.comments = []; p.time = this._time(); this.posts.push(p); };

    // 1. Match Preview posts (4)
    WC2026.fixtures.slice(0, 4).forEach(fx => {
      const txt = Generator.matchPreview(fx);
      add({
        category: "Match Preview", icon: "📅",
        image: Visuals.matchBanner(fx.home, fx.away, { label: `GROUP ${fx.group} · ${fx.date}`, sub: fx.venue }),
        caption: txt.caption, hashtags: txt.hashtags
      });
    });

    // 2. Match Summary posts (4) — full CV → caption → text pipeline
    this.buildImageLibrary().filter(i => i.type === "match").slice(0, 4).forEach(img => {
      const det = Vision.analyze(img);
      const cvCaption = Captioning.caption(img, det);
      const scorers = this._scorers(img, img.result);
      const txt = Generator.matchSummary({
        home: img.home, away: img.away,
        hs: img.result.hs, as_: img.result.as_, scorers, venue: img.venue
      });
      add({
        category: "Match Summary", icon: "📸",
        image: Visuals.matchBanner(img.home, img.away, {
          label: `FULL TIME · ${img.home} ${img.result.hs}-${img.result.as_} ${img.away}`, sub: img.venue
        }),
        caption: txt.caption, hashtags: txt.hashtags,
        vision: Vision.toSpecJSON(det), visionCaption: cvCaption
      });
    });

    // 3. Player Spotlight posts (5)
    WC2026.players.slice(0, 5).forEach(p => {
      const txt = Generator.playerSpotlight(p);
      add({
        category: "Player Spotlight", icon: "🌟",
        image: Visuals.playerThumb(p),
        caption: txt.caption, hashtags: txt.hashtags
      });
    });

    // 4. Stadium posts (4)
    WC2026.stadiums.slice(0, 4).forEach(s => {
      const txt = Generator.stadiumPost(s);
      add({
        category: "Stadium", icon: "🏟️",
        image: Visuals.stadiumCard(s),
        caption: txt.caption, hashtags: txt.hashtags
      });
    });

    // 5. Fan Community posts (poll + quiz + prediction = 3+)
    ["D", "C", "A"].forEach(g => {
      const poll = Generator.fanPoll(g);
      add({
        category: "Fan Community", icon: "📊", kind: "poll",
        image: Visuals.promptCard(`Who wins Group ${g}?`,
          poll.options.map((t, i) => `${String.fromCharCode(65 + i)}. ${t}`), "#5b21b6"),
        caption: poll.caption, hashtags: poll.hashtags,
        poll: { options: poll.options, votes: poll.options.map(() => randInt(50, 1200)) }
      });
    });
    const quiz = Generator.fanQuiz();
    add({
      category: "Fan Community", icon: "🧠", kind: "quiz",
      image: Visuals.promptCard("Quiz Time!", ["A", "B", "C", "D"], "#0f766e"),
      caption: quiz.caption, hashtags: quiz.hashtags, quiz
    });
    const pred = Generator.fanPrediction();
    add({
      category: "Fan Community", icon: "🔮", kind: "prediction",
      image: Visuals.story("Bold Prediction", "Who goes all the way in 2026?", "#b91c1c"),
      caption: pred.caption, hashtags: pred.hashtags
    });

    // Bonus: top-moments collage + research-extension narrative
    add({
      category: "Highlight Reel", icon: "🎬",
      image: Visuals.collage([
        { emoji: "⚽", label: "GOAL", color: "#1a73e8" },
        { emoji: "🧤", label: "SAVE", color: "#16a34a" },
        { emoji: "🎉", label: "CELEBRATION", color: "#db2777" },
        { emoji: "🏆", label: "TROPHY", color: "#ca8a04" }
      ]),
      caption: "🎬 TOP MOMENTS OF THE WEEK!\n\nGoals, saves, celebrations — the World Cup has it all. 🔥\nWhich was your moment of the week? 👇",
      hashtags: Generator.hashtags("TopMoments", "Highlights")
    });
    add(this._narrativePost());

    // Build the Stage-1 image-analysis report rows
    this.buildImageLibrary().forEach(img => {
      const det = Vision.analyze(img);
      this.reportRows.push({
        type: img.type,
        subject: img.player ? img.player.name : img.stadium ? img.stadium.name : (img.team || `${img.home} vs ${img.away}`),
        caption: Captioning.caption(img, det),
        json: Vision.toSpecJSON(det)
      });
    });

    return this.posts;
  },

  /* ---------- Research extension: multimodal narrative ---------- */
  _narrativePost() {
    const imgs = this.buildImageLibrary().filter(i => i.type === "match").slice(0, 3);
    const t = pick(["Brazil", "Argentina", "France"]);
    const story =
      `🧵 THE STORY OF THE MATCH (multimodal narrative)\n\n` +
      `${TEAM_BY_NAME[t].flag} ${t} dominated possession, created multiple chances, ` +
      `scored in the second half, and celebrated with thousands of fans. 🎉\n\n` +
      `Built by stitching a sequence of match images into one temporal story. 📲`;
    return {
      category: "Visual Storytelling", icon: "🧠",
      image: Visuals.story(`${t} — The Full Story`, "Possession → Chances → Goal → Celebration", teamColor(t, 0)),
      caption: story, hashtags: Generator.hashtags(t, "VisualStorytelling")
    };
  },

  /* ---------- helpers ---------- */
  _scorers(img, r) {
    const names = [];
    const poolH = WC2026.players.filter(p => p.team === img.home);
    const poolA = WC2026.players.filter(p => p.team === img.away);
    for (let i = 0; i < r.hs; i++) names.push((pick(poolH) || { name: img.home + " player" }).name + " ⚽");
    for (let i = 0; i < r.as_; i++) names.push((pick(poolA) || { name: img.away + " player" }).name + " ⚽");
    return names;
  },
  _time() {
    const opts = ["Just now", "2m", "15m", "1h", "3h", "Yesterday"];
    return pick(opts);
  }
};

/* =============================================================
   RENDERING
   ============================================================= */
const UI = {
  render() {
    this.renderHeader();
    this.renderFeed("all");
    this.renderAnalytics();
    this.renderReport();
    this.renderMemory();
  },

  renderHeader() {
    document.getElementById("persona-name").textContent = PERSONA.name;
    document.getElementById("persona-handle").textContent = PERSONA.handle;
    document.getElementById("persona-avatar").textContent = PERSONA.avatar;
    document.getElementById("persona-style").textContent = PERSONA.style.join(" · ");
    document.getElementById("stat-posts").textContent = Feed.posts.length;
  },

  renderFeed(filter) {
    const wrap = document.getElementById("feed");
    wrap.innerHTML = "";
    const list = filter === "all" ? Feed.posts : Feed.posts.filter(p => p.category === filter);
    list.forEach(p => wrap.appendChild(this.postCard(p)));
  },

  postCard(p) {
    const el = document.createElement("article");
    el.className = "post";
    el.innerHTML = `
      <div class="post-head">
        <div class="avatar">${PERSONA.avatar}</div>
        <div class="meta">
          <span class="name">${PERSONA.name} <span class="verified">✔</span></span>
          <span class="sub">${PERSONA.handle} · ${p.time}</span>
        </div>
        <span class="badge">${p.icon} ${p.category}</span>
      </div>
      <div class="post-caption">${this._fmt(p.caption)}</div>
      <img class="post-img" src="${p.image}" alt="${p.category}">
      ${p.vision ? `<details class="cv"><summary>🔬 Computer-Vision output (Module 1)</summary>
        <div class="cv-cap">📝 ${p.visionCaption}</div>
        <pre>${JSON.stringify(p.vision, null, 2)}</pre></details>` : ""}
      ${p.poll ? this._pollHTML(p) : ""}
      ${p.quiz ? this._quizHTML(p) : ""}
      <div class="hashtags">${p.hashtags.map(h => `<span>${h}</span>`).join(" ")}</div>
      <div class="post-actions">
        <button class="act like" data-id="${p.id}">❤️ <span>${p.likes.toLocaleString()}</span></button>
        <button class="act cbtn" data-id="${p.id}">💬 <span>${p.comments.length}</span></button>
        <button class="act share">🔁 Share</button>
        <a class="act dl" href="${p.image}" download="wci2026_post_${p.id}.png">⬇️ Image</a>
      </div>
      <div class="comments" id="comments-${p.id}">
        ${p.comments.map(c => this._commentHTML(c)).join("")}
      </div>
      <form class="comment-form" data-id="${p.id}">
        <input class="cname" placeholder="Your name" required>
        <input class="ctext" placeholder="Write a comment… (try mentioning your team!)" required>
        <button type="submit">Post</button>
      </form>`;
    return el;
  },

  _pollHTML(p) {
    const total = p.poll.votes.reduce((a, b) => a + b, 0) || 1;
    return `<div class="poll" data-id="${p.id}">
      ${p.poll.options.map((o, i) => {
        const pct = Math.round(p.poll.votes[i] / total * 100);
        return `<button class="poll-opt" data-id="${p.id}" data-i="${i}">
          <span class="bar" style="width:${pct}%"></span>
          <span class="lbl">${teamFlag(o)} ${o}</span><span class="pct">${pct}%</span>
        </button>`;
      }).join("")}
      <div class="poll-total">${total.toLocaleString()} votes</div>
    </div>`;
  },

  _quizHTML(p) {
    return `<div class="quiz" data-id="${p.id}">
      ${p.quiz.caption.match(/[A-D]\..+/g).map((line, i) =>
        `<button class="quiz-opt" data-id="${p.id}" data-i="${i}">${line}</button>`).join("")}
      <div class="quiz-result"></div>
    </div>`;
  },

  _commentHTML(c) {
    return `<div class="comment ${c.bot ? "bot" : ""}">
      <b>${c.bot ? PERSONA.avatar + " " + PERSONA.name : "👤 " + c.name}</b> ${this._fmt(c.text)}
    </div>`;
  },

  _fmt(t) {
    return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\n/g, "<br>")
            .replace(/(#[A-Za-z0-9]+)/g, '<span class="tag">$1</span>');
  },

  /* ---------- Analytics dashboard ---------- */
  renderAnalytics() {
    const totalLikes = Feed.posts.reduce((a, p) => a + p.likes, 0);
    const byCat = {};
    Feed.posts.forEach(p => byCat[p.category] = (byCat[p.category] || 0) + p.likes);
    document.getElementById("an-likes").textContent = totalLikes.toLocaleString();
    document.getElementById("an-posts").textContent = Feed.posts.length;
    document.getElementById("an-followers").textContent = (1240000 + totalLikes % 5000).toLocaleString();
    const eng = (totalLikes / Feed.posts.length / 9800 * 100).toFixed(1);
    document.getElementById("an-eng").textContent = eng + "%";

    const max = Math.max(...Object.values(byCat));
    const bars = document.getElementById("an-bars");
    bars.innerHTML = Object.entries(byCat).sort((a, b) => b[1] - a[1]).map(([k, v]) =>
      `<div class="anbar"><span class="anlbl">${k}</span>
        <span class="antrack"><span class="anfill" style="width:${v / max * 100}%"></span></span>
        <span class="anval">${v.toLocaleString()}</span></div>`).join("");

    // category filter chips
    const chips = document.getElementById("filters");
    const cats = ["all", ...new Set(Feed.posts.map(p => p.category))];
    chips.innerHTML = cats.map(c =>
      `<button class="chip ${c === "all" ? "on" : ""}" data-cat="${c}">${c === "all" ? "🏠 All" : c}</button>`).join("");
  },

  /* ---------- Stage-1 image analysis report ---------- */
  renderReport() {
    const body = document.getElementById("report-body");
    body.innerHTML = Feed.reportRows.map(r =>
      `<tr><td>${r.type}</td><td>${r.subject}</td><td>${r.caption}</td>
       <td><code>${JSON.stringify(r.json)}</code></td></tr>`).join("");
    document.getElementById("report-count").textContent = Feed.reportRows.length;
  },

  /* ---------- Memory DB viewer ---------- */
  renderMemory() {
    const box = document.getElementById("memory-list");
    const users = MemoryDB.list();
    if (!users.length) { box.innerHTML = `<p class="muted">No followers remembered yet. Comment on a post to be remembered! 🧠</p>`; return; }
    box.innerHTML = users.map(u =>
      `<div class="mem"><b>👤 ${u.user}</b> · ❤️ ${u.favorite_team || "—"}
        <div class="muted">"${u.last_comment || ""}"</div></div>`).join("");
  }
};

/* =============================================================
   EVENTS
   ============================================================= */
document.addEventListener("click", (e) => {
  // like
  const like = e.target.closest(".like");
  if (like) {
    const p = Feed.posts.find(x => x.id == like.dataset.id);
    p.likes++; like.querySelector("span").textContent = p.likes.toLocaleString();
    UI.renderAnalytics();
    document.querySelector(`.chip[data-cat="all"]`).classList.add("on");
    return;
  }
  // filter chips
  const chip = e.target.closest(".chip");
  if (chip) {
    document.querySelectorAll(".chip").forEach(c => c.classList.remove("on"));
    chip.classList.add("on");
    UI.renderFeed(chip.dataset.cat);
    return;
  }
  // poll vote
  const popt = e.target.closest(".poll-opt");
  if (popt) {
    const p = Feed.posts.find(x => x.id == popt.dataset.id);
    p.poll.votes[+popt.dataset.i]++;
    popt.closest(".post").querySelector(".poll").outerHTML = UI._pollHTML(p);
    return;
  }
  // quiz answer
  const qopt = e.target.closest(".quiz-opt");
  if (qopt) {
    const p = Feed.posts.find(x => x.id == qopt.dataset.id);
    const correct = +qopt.dataset.i === p.quiz.answer;
    const box = qopt.closest(".quiz").querySelector(".quiz-result");
    box.textContent = correct ? "✅ Correct! Nice one! 🎉" : "❌ Not quite — try the next quiz!";
    box.className = "quiz-result " + (correct ? "ok" : "no");
    return;
  }
});

// comment submit → personalized AI reply + memory
document.addEventListener("submit", (e) => {
  const form = e.target.closest(".comment-form");
  if (!form) return;
  e.preventDefault();
  const p = Feed.posts.find(x => x.id == form.dataset.id);
  const name = form.querySelector(".cname").value.trim();
  const text = form.querySelector(".ctext").value.trim();
  if (!name || !text) return;

  p.comments.push({ name, text, bot: false });
  const profile = MemoryDB.remember(name, { last_comment: text });

  // AI actor replies, personalized using memory
  setTimeout(() => {
    p.comments.push({ name: PERSONA.name, text: Generator.personalizedReply(profile), bot: true });
    document.getElementById(`comments-${p.id}`).innerHTML = p.comments.map(c => UI._commentHTML(c)).join("");
    UI.renderMemory();
  }, 500);

  document.getElementById(`comments-${p.id}`).innerHTML = p.comments.map(c => UI._commentHTML(c)).join("");
  form.reset();
});

// regenerate button
document.addEventListener("DOMContentLoaded", () => {
  Feed.generateAll();
  UI.render();
  document.getElementById("btn-regen").addEventListener("click", () => {
    Feed.generateAll(); UI.render();
  });
  document.getElementById("btn-clear-mem").addEventListener("click", () => {
    MemoryDB.clear(); UI.renderMemory();
  });
  // tabs
  document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(x => x.classList.remove("on"));
    document.querySelectorAll(".panel").forEach(x => x.classList.remove("on"));
    t.classList.add("on");
    document.getElementById(t.dataset.panel).classList.add("on");
  }));
});
