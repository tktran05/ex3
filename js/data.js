/* =============================================================
   WorldCup Insider 2026 — Dataset
   FIFA World Cup 2026 (USA · Canada · Mexico) — 48 teams
   Used by all AI modules as the "knowledge base".
   ============================================================= */

const WC2026 = {
  tournament: {
    name: "FIFA World Cup 2026",
    hosts: ["United States", "Canada", "Mexico"],
    teams: 48,
    dates: "11 June – 19 July 2026",
    slogan: "We Are 26"
  },

  /* ---- National teams (subset, with brand colors + flag) ---- */
  teams: [
    { name: "Argentina",     flag: "🇦🇷", group: "C", colors: ["#75AADB", "#FFFFFF"], fifaRank: 1,  nickname: "La Albiceleste" },
    { name: "France",        flag: "🇫🇷", group: "F", colors: ["#002395", "#ED2939"], fifaRank: 2,  nickname: "Les Bleus" },
    { name: "Spain",         flag: "🇪🇸", group: "B", colors: ["#AA151B", "#F1BF00"], fifaRank: 3,  nickname: "La Roja" },
    { name: "England",       flag: "🏴", group: "D", colors: ["#FFFFFF", "#CF081F"], fifaRank: 4,  nickname: "Three Lions" },
    { name: "Brazil",        flag: "🇧🇷", group: "C", colors: ["#009C3B", "#FFDF00"], fifaRank: 5,  nickname: "Seleção" },
    { name: "Portugal",      flag: "🇵🇹", group: "E", colors: ["#006600", "#FF0000"], fifaRank: 6,  nickname: "Seleção das Quinas" },
    { name: "Netherlands",   flag: "🇳🇱", group: "A", colors: ["#FF6600", "#21468B"], fifaRank: 7,  nickname: "Oranje" },
    { name: "Croatia",       flag: "🇭🇷", group: "D", colors: ["#FF0000", "#FFFFFF"], fifaRank: 8,  nickname: "Vatreni" },
    { name: "Germany",       flag: "🇩🇪", group: "B", colors: ["#000000", "#DD0000"], fifaRank: 9,  nickname: "Die Mannschaft" },
    { name: "Belgium",       flag: "🇧🇪", group: "F", colors: ["#000000", "#FDDA24"], fifaRank: 10, nickname: "Red Devils" },
    { name: "USA",           flag: "🇺🇸", group: "D", colors: ["#0A3161", "#B31942"], fifaRank: 11, nickname: "Stars and Stripes" },
    { name: "Mexico",        flag: "🇲🇽", group: "A", colors: ["#006847", "#CE1126"], fifaRank: 14, nickname: "El Tri" },
    { name: "Uruguay",       flag: "🇺🇾", group: "E", colors: ["#7CB9E8", "#001489"], fifaRank: 15, nickname: "La Celeste" },
    { name: "Austria",       flag: "🇦🇹", group: "C", colors: ["#ED2939", "#FFFFFF"], fifaRank: 22, nickname: "Das Team" },
    { name: "Canada",        flag: "🇨🇦", group: "A", colors: ["#FF0000", "#FFFFFF"], fifaRank: 28, nickname: "Les Rouges" },
    { name: "Australia",     flag: "🇦🇺", group: "D", colors: ["#00843D", "#FFCD00"], fifaRank: 24, nickname: "Socceroos" },
    { name: "Paraguay",      flag: "🇵🇾", group: "D", colors: ["#D52B1E", "#0038A8"], fifaRank: 36, nickname: "La Albirroja" },
    { name: "Turkey",        flag: "🇹🇷", group: "D", colors: ["#E30A17", "#FFFFFF"], fifaRank: 26, nickname: "Ay-Yıldızlılar" }
  ],

  /* ---- Star players with stats + fun facts ---- */
  players: [
    { name: "Lionel Messi",        team: "Argentina", pos: "Forward",    age: 38, number: 10,
      stats: { caps: 191, goals: 112, assists: 58 },
      facts: ["8-time Ballon d'Or winner", "Led Argentina to the 2022 World Cup title", "All-time top scorer for Argentina"] },
    { name: "Kylian Mbappé",       team: "France",    pos: "Forward",    age: 27, number: 10,
      stats: { caps: 86, goals: 48, assists: 30 },
      facts: ["World Cup winner in 2018 at age 19", "Scored a hat-trick in the 2022 final", "One of the fastest players in world football"] },
    { name: "Lamine Yamal",        team: "Spain",     pos: "Winger",     age: 18, number: 19,
      stats: { caps: 25, goals: 9, assists: 14 },
      facts: ["Euro 2024 champion as a teenager", "Youngest goalscorer in Euros history", "Product of La Masia academy"] },
    { name: "Jude Bellingham",     team: "England",   pos: "Midfielder", age: 22, number: 10,
      stats: { caps: 42, goals: 8, assists: 9 },
      facts: ["Real Madrid midfield engine", "His #22 shirt was retired at Birmingham City", "Won the Champions League in 2024"] },
    { name: "Vinícius Júnior",     team: "Brazil",    pos: "Winger",     age: 25, number: 7,
      stats: { caps: 40, goals: 6, assists: 8 },
      facts: ["Champions League final scorer in 2024", "Known for electric dribbling", "Real Madrid's left-wing talisman"] },
    { name: "Cristiano Ronaldo",   team: "Portugal",  pos: "Forward",    age: 41, number: 7,
      stats: { caps: 217, goals: 138, assists: 47 },
      facts: ["All-time top scorer in men's international football", "5-time Ballon d'Or winner", "Played in a record number of World Cups"] },
    { name: "Harry Kane",          team: "England",   pos: "Striker",    age: 32, number: 9,
      stats: { caps: 105, goals: 69, assists: 20 },
      facts: ["England's all-time top scorer", "2018 World Cup Golden Boot winner", "Prolific from open play and penalties"] },
    { name: "Christian Pulisic",   team: "USA",       pos: "Winger",     age: 27, number: 10,
      stats: { caps: 78, goals: 32, assists: 25 },
      facts: ["Captain America of US soccer", "First American to score in a Champions League knockout", "Face of the US team on home soil"] }
  ],

  /* ---- Host stadiums ---- */
  stadiums: [
    { name: "MetLife Stadium",        city: "New York / New Jersey", country: "USA",    capacity: 82500, opened: 2010,
      architecture: "Modern bowl with dual-team aluminium-louvre façade that lights up in team colours.",
      note: "Hosts the 2026 World Cup Final." },
    { name: "Estadio Azteca",         city: "Mexico City",           country: "Mexico", capacity: 87000, opened: 1966,
      architecture: "Iconic concrete bowl, one of the largest and most storied stadiums in the world.",
      note: "Only stadium to host three different World Cups (1970, 1986, 2026)." },
    { name: "SoFi Stadium",           city: "Los Angeles",           country: "USA",    capacity: 70000, opened: 2020,
      architecture: "Translucent ETFE canopy roof and a 360° dual-sided videoboard (the Infinity Screen).",
      note: "Most expensive stadium ever built." },
    { name: "AT&T Stadium",           city: "Dallas",                country: "USA",    capacity: 80000, opened: 2009,
      architecture: "Retractable roof with one of the world's largest column-free interiors and a giant centre-hung screen.",
      note: "Nicknamed 'Jerry World'." },
    { name: "BC Place",               city: "Vancouver",             country: "Canada", capacity: 54500, opened: 1983,
      architecture: "Cable-supported retractable fabric roof, the largest of its kind in the world.",
      note: "Vancouver's downtown waterfront landmark." },
    { name: "Estadio BBVA",           city: "Monterrey",             country: "Mexico", capacity: 53500, opened: 2015,
      architecture: "Steel lattice 'El Gigante de Acero' framing views of the Cerro de la Silla mountain.",
      note: "Widely praised as one of Latin America's best venues." }
  ],

  /* ---- Simulated fixtures used for previews / summaries ---- */
  fixtures: [
    { home: "England",   away: "Croatia",   group: "D", date: "2026-06-18", venue: "AT&T Stadium" },
    { home: "Argentina", away: "Austria",   group: "C", date: "2026-06-19", venue: "MetLife Stadium" },
    { home: "Brazil",    away: "Argentina", group: "C", date: "2026-06-22", venue: "Estadio Azteca" },
    { home: "France",    away: "Belgium",   group: "F", date: "2026-06-20", venue: "SoFi Stadium" },
    { home: "Spain",     away: "Germany",   group: "B", date: "2026-06-21", venue: "BC Place" },
    { home: "USA",       away: "Australia",  group: "D", date: "2026-06-23", venue: "SoFi Stadium" },
    { home: "Portugal",  away: "Uruguay",   group: "E", date: "2026-06-24", venue: "Estadio BBVA" },
    { home: "Mexico",    away: "Netherlands", group: "A", date: "2026-06-25", venue: "Estadio Azteca" }
  ],

  /* ---- Groups for polls/quizzes ---- */
  groups: {
    A: ["Mexico", "Netherlands", "Canada"],
    B: ["Spain", "Germany"],
    C: ["Argentina", "Brazil", "Austria"],
    D: ["England", "Croatia", "USA", "Australia", "Paraguay", "Turkey"],
    E: ["Portugal", "Uruguay"],
    F: ["France", "Belgium"]
  }
};

/* Helper lookups */
const TEAM_BY_NAME = Object.fromEntries(WC2026.teams.map(t => [t.name, t]));
function teamColor(name, i = 0) {
  const t = TEAM_BY_NAME[name];
  return t ? t.colors[i % t.colors.length] : "#1a73e8";
}
function teamFlag(name) {
  const t = TEAM_BY_NAME[name];
  return t ? t.flag : "⚽";
}
function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function randInt(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
