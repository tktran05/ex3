/* =============================================================
   MODULE 3 — Social-Media Text Generator (simulated GPT/Llama/Gemma)
   -------------------------------------------------------------
   Drives the "WorldCup Insider 2026" persona. A real build would
   send the persona system-prompt + caption to an LLM; here we use
   template + variation engines that respect the persona's tone:
     - Enthusiastic, friendly, knowledgeable
     - Short sentences, emojis allowed, high engagement
   ============================================================= */

const PERSONA = {
  name: "WorldCup Insider 2026",
  handle: "@worldcup_insider26",
  avatar: "🌍⚽",
  style: ["Enthusiastic", "Friendly", "Knowledgeable"],
  audience: "Football fans aged 18–35",
  systemPrompt:
    "You are WorldCup Insider 2026, a football journalist and superfan. " +
    "Write short, punchy, upbeat social posts. Use emojis. Drive engagement."
};

const Generator = {
  /* -------- Hashtags -------- */
  hashtags(...topics) {
    const base = ["#WorldCup2026", "#FIFAWorldCup", "#WeAre26", "#Football"];
    const extra = topics
      .filter(Boolean)
      .map(t => "#" + t.replace(/[^A-Za-z0-9]/g, ""));
    return [...new Set([...extra, ...base])].slice(0, 6);
  },

  /* -------- 1. Match Preview -------- */
  matchPreview(fx) {
    const h = TEAM_BY_NAME[fx.home], a = TEAM_BY_NAME[fx.away];
    const intro = pick([
      `🚨 MATCHDAY INCOMING! ${h.flag} ${fx.home} face ${a.flag} ${fx.away}!`,
      `⚡ Get ready! ${fx.home} ${h.flag} take on ${fx.away} ${a.flag} in Group ${fx.group}!`,
      `🔥 Tomorrow ${fx.home} meet ${fx.away}. This one is going to be special!`
    ]);
    const body = pick([
      `${fx.home} enter the match after a strong qualifying campaign and look razor-sharp. ${fx.away} won't go down easy though — expect fireworks at ${fx.venue}. 🏟️`,
      `Two proud footballing nations, one massive Group ${fx.group} clash. ${fx.home} bring firepower up front, ${fx.away} bring grit and pace. Who takes the points? 👀`,
      `${fx.away} have been the surprise package, but ${fx.home} are red-hot. A win here could decide the group. Tactical battle at ${fx.venue} awaits! 🎯`
    ]);
    const cta = pick([
      "Who's winning this one? Drop your score prediction below! 👇",
      "Tell us your starting XI in the comments! 🗣️",
      "Are you team home or team away? React now! ❤️🔥"
    ]);
    return {
      caption: `${intro}\n\n${body}\n\n${cta}`,
      hashtags: this.hashtags(fx.home, fx.away, fx.venue.split(" ")[0])
    };
  },

  /* -------- 2. Match Summary -------- */
  matchSummary(result) {
    const { home, away, hs, as_, scorers, venue } = result;
    const winner = hs > as_ ? home : as_ > hs ? away : null;
    const head = winner
      ? `${TEAM_BY_NAME[winner].flag} ${winner.toUpperCase()} ${pick(["WIN!", "TAKE IT!", "GET THE JOB DONE!"])}`
      : `🤝 HONOURS EVEN!`;
    const scoreline = winner
      ? `${winner} defeated ${winner === home ? away : home} ${Math.max(hs, as_)}-${Math.min(hs, as_)} in a dramatic encounter at ${venue}. 🔥`
      : `${home} and ${away} shared the spoils in a ${hs}-${as_} thriller at ${venue}. ⚖️`;
    const detail = scorers.length
      ? `⚽ On the scoresheet: ${scorers.join(", ")}.`
      : `A tense, cagey affair decided by the finest of margins.`;
    return {
      caption: `${head}\n\n${scoreline}\n${detail}\n\nWhat a match! Did your team deliver today? 🙌`,
      hashtags: this.hashtags(home, away, `${home}vs${away}`)
    };
  },

  /* -------- 3. Player Spotlight -------- */
  playerSpotlight(p) {
    const fact = pick(p.facts);
    return {
      caption:
        `🌟 PLAYER SPOTLIGHT 🌟\n\n` +
        `${TEAM_BY_NAME[p.team].flag} ${p.name} — ${p.pos} | #${p.number} | ${p.team}\n\n` +
        `📊 ${p.stats.caps} caps · ${p.stats.goals} goals · ${p.stats.assists} assists\n` +
        `💡 Did you know? ${fact}.\n\n` +
        `At ${p.age}, he's ready to light up World Cup 2026. Is he your pick for the Golden Ball? 🏆`,
      hashtags: this.hashtags(p.name, p.team)
    };
  },

  /* -------- 4. Stadium Post (travel style) -------- */
  stadiumPost(s) {
    return {
      caption:
        `🏟️ VENUE GUIDE: ${s.name} ✈️\n\n` +
        `📍 ${s.city}, ${s.country}\n` +
        `👥 Capacity: ${s.capacity.toLocaleString()}\n` +
        `🏗️ ${s.architecture}\n` +
        `⭐ ${s.note}\n\n` +
        `Imagine the roar inside here on matchday! Would you travel to ${s.city} for a game? 🌎`,
      hashtags: this.hashtags(s.name, s.city, s.country)
    };
  },

  /* -------- 5. Fan Community (poll / quiz / prediction) -------- */
  fanPoll(group) {
    const teams = WC2026.groups[group];
    const options = teams.slice(0, 4).map((t, i) =>
      `${String.fromCharCode(65 + i)}. ${TEAM_BY_NAME[t].flag} ${t}`
    );
    return {
      kind: "poll",
      caption: `📊 FAN POLL TIME!\n\nWho will win Group ${group}? 🤔\n\n${options.join("\n")}\n\nVote now and tell us why! 👇`,
      options: teams.slice(0, 4),
      hashtags: this.hashtags(`Group${group}`, "Poll")
    };
  },

  fanQuiz() {
    const quizzes = [
      { q: "Which stadium hosts the 2026 World Cup Final? 🏆", opts: ["MetLife Stadium", "SoFi Stadium", "Estadio Azteca", "AT&T Stadium"], answer: 0 },
      { q: "Which country is NOT a 2026 host? 🌎", opts: ["USA", "Canada", "Mexico", "Brazil"], answer: 3 },
      { q: "How many teams play at World Cup 2026? ⚽", opts: ["32", "40", "48", "64"], answer: 2 }
    ];
    const z = pick(quizzes);
    const opts = z.opts.map((o, i) => `${String.fromCharCode(65 + i)}. ${o}`);
    return {
      kind: "quiz",
      caption: `🧠 QUIZ TIME!\n\n${z.q}\n\n${opts.join("\n")}\n\nComment your answer — no Googling! 😉`,
      answer: z.answer,
      hashtags: this.hashtags("Quiz", "Trivia")
    };
  },

  fanPrediction() {
    const t = pick(WC2026.teams);
    return {
      kind: "prediction",
      caption:
        `🔮 BOLD PREDICTION!\n\n${t.flag} ${t.name} (${t.nickname}) to go far in 2026. ` +
        `Ranked #${t.fifaRank} in the world and full of belief. 💪\n\nAgree or disagree? Let us hear it! 🗣️`,
      hashtags: this.hashtags(t.name, "Prediction")
    };
  },

  /* -------- Personalized reply (Advanced Challenge) -------- */
  personalizedReply(user) {
    if (!user || !user.favorite_team) {
      return pick([
        "Great point! ⚽ What's your World Cup prediction? 🌍",
        "Love the energy! 🔥 Who's your team to win it all?",
        "Thanks for joining the conversation! 🙌"
      ]);
    }
    const t = TEAM_BY_NAME[user.favorite_team];
    const flag = t ? t.flag : "⚽";
    return pick([
      `Hi ${user.name}! ${flag} ${user.favorite_team} looked strong recently. Do you think they'll top their group? 🤔`,
      `Hey ${user.name}! Always love a ${user.favorite_team} fan ${flag}. Big things coming this World Cup! 🚀`,
      `${user.name}, ${user.favorite_team} ${flag} have the squad to surprise everyone. Backing them all the way? 💪`
    ]);
  }
};
