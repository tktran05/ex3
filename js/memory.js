/* =============================================================
   ADVANCED CHALLENGE — Memory Database
   -------------------------------------------------------------
   Persists a per-follower profile so future replies are
   personalized. Schema matches the spec:
     { "user": "John", "favorite_team": "Brazil", "last_comment": "Brazil will win!" }
   Stored in localStorage (a tiny embedded DB for the demo).
   ============================================================= */

const MemoryDB = {
  KEY: "wci2026_memory",

  _all() {
    try { return JSON.parse(localStorage.getItem(this.KEY)) || {}; }
    catch { return {}; }
  },
  _save(db) { localStorage.setItem(this.KEY, JSON.stringify(db)); },

  remember(user, fields) {
    const db = this._all();
    db[user] = { user, ...(db[user] || {}), ...fields, updated: Date.now() };
    // Infer favourite team from the comment if not set
    if (!db[user].favorite_team && fields.last_comment) {
      const found = WC2026.teams.find(t =>
        new RegExp(`\\b${t.name}\\b`, "i").test(fields.last_comment));
      if (found) db[user].favorite_team = found.name;
    }
    this._save(db);
    return db[user];
  },

  get(user) { return this._all()[user] || null; },
  list() { return Object.values(this._all()); },
  clear() { localStorage.removeItem(this.KEY); }
};
