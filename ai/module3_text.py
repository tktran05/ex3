"""
MODULE 3 — Social-media Text Generator  (Google Gemini)
-------------------------------------------------------
Drives the 'WorldCup Insider 2026' persona. Each method builds a prompt
(system persona + structured context from CV/captioning + knowledge base)
and asks Gemini for a ready-to-post caption. If the API key is missing or a
call fails, a persona-consistent template fallback is used so the pipeline
never breaks.
"""
from __future__ import annotations
import json
import random
import config
from data import TEAM_BY_NAME, GROUPS, team_flag
from persona import SYSTEM_PROMPT


def _hashtags(*topics):
    base = ["#WorldCup2026", "#FIFAWorldCup", "#WeAre26", "#Football"]
    extra = ["#" + "".join(ch for ch in t if ch.isalnum()) for t in topics if t]
    seen, out = set(), []
    for h in extra + base:
        if h.lower() not in seen:
            seen.add(h.lower()); out.append(h)
    return out[:6]


class TextGenerator:
    def __init__(self):
        self.enabled = False
        self.model = None
        if config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(
                    config.GEMINI_MODEL, system_instruction=SYSTEM_PROMPT
                )
                self.enabled = True
            except Exception as e:
                print(f"[Gemini] disabled ({e}); using template fallback.")

    # ---- core call ----------------------------------------------------
    def _gen(self, user_prompt: str, fallback: str, retries: int = 3) -> str:
        if not self.enabled:
            return fallback
        import time
        for attempt in range(retries):
            try:
                resp = self.model.generate_content(user_prompt)
                txt = (resp.text or "").strip()
                return txt or fallback
            except Exception as e:
                msg = str(e)
                is_rate = "429" in msg or "quota" in msg.lower() or "rate" in msg.lower()
                if is_rate and attempt < retries - 1:
                    wait = 5 * (attempt + 1)
                    print(f"[Gemini] rate-limited, retrying in {wait}s ...")
                    time.sleep(wait)
                    continue
                print(f"[Gemini] generation failed ({e}); fallback used.")
                return fallback
        return fallback

    # ================= POST TYPES =================

    # 1 ---- Match preview ----
    def match_preview(self, fx):
        h, a = fx["home"], fx["away"]
        prompt = (
            f"Write a Match Preview post for {h} vs {a} (Group {fx['group']}) at "
            f"{fx['venue']} on {fx['date']}. Mention both teams' form and build hype. "
            "3-5 short lines. End with a question. Do not add hashtags."
        )
        fallback = (
            f"🚨 MATCHDAY! {team_flag(h)} {h} face {team_flag(a)} {a} in Group {fx['group']}!\n\n"
            f"{h} arrive in red-hot form, but {a} won't make it easy at {fx['venue']}. 🔥\n\n"
            "Who's taking the three points? Drop your score below! 👇"
        )
        return {"caption": self._gen(prompt, fallback),
                "hashtags": _hashtags(h, a, fx["venue"].split()[0])}

    # 2 ---- Match summary (uses CV + caption) ----
    def match_summary(self, ctx):
        prompt = (
            "Write a Match Summary post from this analysed match photo.\n"
            f"Vision JSON: {json.dumps(ctx['vision'])}\n"
            f"Image caption: {ctx['caption']}\n"
            f"Result: {ctx['home']} {ctx['hs']}-{ctx['as_']} {ctx['away']} at {ctx['venue']}. "
            f"Scorers: {', '.join(ctx['scorers']) or 'n/a'}.\n"
            "Start with the result like 'X defeated Y 2-1 in a dramatic encounter'. "
            "3-4 short lines, emojis, end with a question. No hashtags."
        )
        h, a, hs, as_ = ctx["home"], ctx["away"], ctx["hs"], ctx["as_"]
        winner = h if hs > as_ else a if as_ > hs else None
        if winner:
            line = (f"{winner} defeated {a if winner == h else h} "
                    f"{max(hs, as_)}-{min(hs, as_)} in a dramatic encounter at {ctx['venue']}! 🔥")
        else:
            line = f"{h} and {a} shared the spoils in a {hs}-{as_} thriller at {ctx['venue']}! ⚖️"
        fallback = f"📸 FULL TIME!\n\n{line}\n⚽ {', '.join(ctx['scorers']) or 'A tense battle.'}\n\nDid your team deliver today? 🙌"
        return {"caption": self._gen(prompt, fallback),
                "hashtags": _hashtags(h, a, f"{h}vs{a}")}

    # 3 ---- Player spotlight ----
    def player_spotlight(self, p):
        s = p["stats"]
        prompt = (
            f"Write a Player Spotlight post for {p['name']} ({p['pos']}, {p['team']}, #{p['number']}).\n"
            f"Stats: {s['caps']} caps, {s['goals']} goals, {s['assists']} assists. Age {p['age']}.\n"
            f"Facts: {'; '.join(p['facts'])}.\n"
            "Include a profile line, the stats, one fun fact. 4-5 short lines, emojis, end with a question. No hashtags."
        )
        fallback = (
            f"🌟 PLAYER SPOTLIGHT 🌟\n\n{team_flag(p['team'])} {p['name']} — {p['pos']} · #{p['number']} · {p['team']}\n"
            f"📊 {s['caps']} caps · {s['goals']} goals · {s['assists']} assists\n"
            f"💡 {random.choice(p['facts'])}.\n\nIs he your Golden Ball pick? 🏆"
        )
        return {"caption": self._gen(prompt, fallback), "hashtags": _hashtags(p["name"], p["team"])}

    # 4 ---- Stadium (travel style) ----
    def stadium_post(self, s):
        prompt = (
            f"Write a travel-style Stadium post about {s['name']} in {s['city']}, {s['country']}.\n"
            f"Capacity {s['capacity']}. Architecture: {s['architecture']} Note: {s['note']}\n"
            "Make fans want to visit. 4-5 short lines, emojis, end with a question. No hashtags."
        )
        fallback = (
            f"🏟️ VENUE GUIDE: {s['name']} ✈️\n\n📍 {s['city']}, {s['country']}\n"
            f"👥 Capacity: {s['capacity']:,}\n🏗️ {s['architecture']}\n⭐ {s['note']}\n\n"
            f"Would you travel to {s['city']} for a game? 🌎"
        )
        return {"caption": self._gen(prompt, fallback), "hashtags": _hashtags(s["name"], s["city"], s["country"])}

    # 5 ---- Fan community ----
    def fan_poll(self, group):
        teams = GROUPS[group][:4]
        opts = [f"{chr(65+i)}. {team_flag(t)} {t}" for i, t in enumerate(teams)]
        prompt = (f"Write a short fan POLL post asking who wins Group {group}. "
                  f"Options:\n" + "\n".join(opts) + "\nEnd asking people to vote. No hashtags.")
        fallback = f"📊 FAN POLL!\n\nWho will win Group {group}? 🤔\n\n" + "\n".join(opts) + "\n\nVote now! 👇"
        return {"kind": "poll", "options": teams,
                "caption": self._gen(prompt, fallback), "hashtags": _hashtags(f"Group{group}", "Poll")}

    def fan_quiz(self):
        quizzes = [
            {"q": "Which stadium hosts the 2026 World Cup Final? 🏆",
             "opts": ["MetLife Stadium", "SoFi Stadium", "Estadio Azteca", "AT&T Stadium"], "answer": 0},
            {"q": "Which country is NOT a 2026 host? 🌎",
             "opts": ["USA", "Canada", "Mexico", "Brazil"], "answer": 3},
            {"q": "How many teams play at World Cup 2026? ⚽",
             "opts": ["32", "40", "48", "64"], "answer": 2},
        ]
        z = random.choice(quizzes)
        opts = [f"{chr(65+i)}. {o}" for i, o in enumerate(z["opts"])]
        prompt = (f"Write a fun fan QUIZ post. Question: {z['q']} Options:\n" + "\n".join(opts) +
                  "\nAsk people to comment their answer. No hashtags, do not reveal the answer.")
        fallback = f"🧠 QUIZ TIME!\n\n{z['q']}\n\n" + "\n".join(opts) + "\n\nComment your answer! 😉"
        return {"kind": "quiz", "answer": z["answer"], "options": z["opts"],
                "caption": self._gen(prompt, fallback), "hashtags": _hashtags("Quiz", "Trivia")}

    def fan_prediction(self):
        t = random.choice(list(TEAM_BY_NAME.values()))
        prompt = (f"Write a bold PREDICTION post about {t['name']} ({t['nickname']}, FIFA rank #{t['rank']}) "
                  "doing well at World Cup 2026. 3 short lines, emojis, end asking agree or disagree. No hashtags.")
        fallback = (f"🔮 BOLD PREDICTION!\n\n{t['flag']} {t['name']} ({t['nickname']}) to go far in 2026. "
                    f"Ranked #{t['rank']} and full of belief. 💪\n\nAgree or disagree? 🗣️")
        return {"kind": "prediction", "caption": self._gen(prompt, fallback),
                "hashtags": _hashtags(t["name"], "Prediction")}

    # ================= PHOTO-DRIVEN POSTS =================
    # Build a post directly from the user's real image (BLIP caption + YOLO json).
    def from_photo(self, post_type, blip_caption, vision, hints=None):
        hints = hints or {}
        team = vision.get("team")
        ctx = f'Image description (from BLIP): "{blip_caption}". Vision detection: {json.dumps(vision)}.'

        if post_type == "match":
            prompt = (f"You are looking at a real World Cup match photo. {ctx}\n"
                      "Write a short, exciting Match post describing what is happening in THIS photo "
                      "(action, the team in focus, the atmosphere). 3-4 short lines, emojis, end with a "
                      "question. Do not invent an exact scoreline. No hashtags.")
            fb = (f"📸 WHAT A MOMENT!\n\n{blip_caption}. "
                  + (f"{team_flag(team)} {team} right in the thick of it! 🔥\n\n" if team else "Pure World Cup drama! 🔥\n\n")
                  + "What's your caption for this shot? 👇")
            tags = _hashtags(team or "", "MatchDay")

        elif post_type == "player":
            name = hints.get("name") or "this star"
            db = hints.get("db")
            stat_line = ""
            if db:
                s = db["stats"]
                stat_line = (f" Known stats: {s['caps']} caps, {s['goals']} goals, {s['assists']} assists; "
                             f"plays {db['pos']} for {db['team']}; facts: {'; '.join(db['facts'])}.")
            prompt = (f"You are looking at a real photo of footballer {name}. {ctx}{stat_line}\n"
                      "Write a Player Spotlight post: a profile line, the stats if given, one fun fact. "
                      "4-5 short lines, emojis, end with a question. No hashtags.")
            if db:
                s = db["stats"]
                fb = (f"🌟 PLAYER SPOTLIGHT 🌟\n\n{team_flag(db['team'])} {db['name']} — {db['pos']} · {db['team']}\n"
                      f"📊 {s['caps']} caps · {s['goals']} goals · {s['assists']} assists\n"
                      f"💡 {db['facts'][0]}.\n\nIs he your Golden Ball pick? 🏆")
            else:
                fb = (f"🌟 PLAYER SPOTLIGHT 🌟\n\n{name} lighting it up at World Cup 2026! ⚽\n"
                      f"{blip_caption}.\n\nWhat do you love about his game? 👇")
            tags = _hashtags(hints.get("name") or "Player", db["team"] if db else "WorldCup")

        elif post_type == "stadium":
            prompt = (f"You are looking at a real photo of a football stadium. {ctx}\n"
                      "Write a travel-style Stadium post inviting fans to visit. Describe the look/atmosphere "
                      "from the photo. 4-5 short lines, emojis, end with a question. No hashtags.")
            fb = (f"🏟️ VENUE VIBES ✈️\n\n{blip_caption}.\nImagine the roar inside on matchday! 🔊\n\n"
                  "Would you travel here for a game? 🌎")
            tags = _hashtags("Stadium", "Travel")

        elif post_type == "team":
            prompt = (f"You are looking at a real national-team photo. {ctx}\n"
                      "Write a hype Team post about the squad in the picture. 3-4 short lines, emojis, "
                      "end with a question. No hashtags.")
            fb = (f"📸 SQUAD GOALS!\n\n{blip_caption}. "
                  + (f"{team_flag(team)} {team} ready for battle! 💪\n\n" if team else "Ready for World Cup glory! 💪\n\n")
                  + "How far do they go in 2026? 👇")
            tags = _hashtags(team or "Team", "Squad")

        else:  # fan
            prompt = (f"You are looking at a real photo of football fans. {ctx}\n"
                      "Write a fun Fan post celebrating the supporters in the picture. 3-4 short lines, "
                      "emojis, end with a question. No hashtags.")
            fb = (f"🎉 FANS BRINGING THE NOISE!\n\n{blip_caption}.\nThis is what the World Cup is all about! ❤️\n\n"
                  "Tag a fan who needs to see this! 👇")
            tags = _hashtags("Fans", "WorldCup")

        return {"caption": self._gen(prompt, fb), "hashtags": tags}

    # ---- Advanced: personalized reply (memory) ----
    def personalized_reply(self, user_profile, comment_text):
        name = user_profile.get("user", "friend") if user_profile else "friend"
        fav = user_profile.get("favorite_team") if user_profile else None
        prompt = (
            f"A follower named {name} commented: \"{comment_text}\".\n"
            + (f"You remember their favourite team is {fav}. Personalise the reply. " if fav else "")
            + "Reply in 1-2 short friendly sentences as WorldCup Insider 2026, with an emoji and a follow-up question."
        )
        if fav:
            fallback = f"Hi {name}! {team_flag(fav)} {fav} are looking strong. Think they'll top their group? 🤔"
        else:
            fallback = f"Great point, {name}! ⚽ What's your World Cup prediction? 🌍"
        return self._gen(prompt, fallback)


if __name__ == "__main__":
    g = TextGenerator()
    print("Gemini enabled:", g.enabled)
    from data import FIXTURES
    print(g.match_preview(FIXTURES[0])["caption"])
