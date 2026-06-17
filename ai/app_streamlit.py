"""
STAGE 3 — Social-network page (Streamlit)
-----------------------------------------
Loads the generated posts and presents the AI actor's page: timeline,
likes, comments with personalised AI replies (Gemini + memory DB),
polls, quizzes and an analytics dashboard.

Run:
    streamlit run app_streamlit.py
(Run generate_posts.py first to create output/posts.json)
"""
from __future__ import annotations
import json
import streamlit as st
import pandas as pd

import config
from persona import PERSONA
from memory_db import MemoryDB

st.set_page_config(page_title="WorldCup Insider 2026", page_icon="🌍", layout="centered")


@st.cache_data
def load_posts():
    if not config.POSTS_JSON.exists():
        return None
    return json.loads(config.POSTS_JSON.read_text(encoding="utf-8"))


@st.cache_resource
def get_text_generator():
    from module3_text import TextGenerator
    return TextGenerator()


def get_memory():
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryDB()
    return st.session_state.memory


data = load_posts()

# ---------- Header ----------
st.markdown(
    f"""<div style='background:linear-gradient(90deg,#0b1530,#10243f);padding:18px;border-radius:14px'>
    <h2 style='margin:0;color:#fff'>{PERSONA['avatar']} {PERSONA['name']}
    <span style='font-size:14px;color:#9cf'>✔ AI Actor</span></h2>
    <div style='color:#9cf'>{PERSONA['handle']} · {' · '.join(PERSONA['style'])} · {PERSONA['audience']}</div>
    </div>""", unsafe_allow_html=True)

if not data:
    st.warning("No posts found. Run **`python generate_posts.py`** first to generate content.")
    st.stop()

posts = data["posts"]

tab_feed, tab_analytics, tab_report, tab_memory = st.tabs(
    ["📰 Timeline", "📈 Analytics", "🔬 Image Report", "🧠 Memory DB"])

# ================= TIMELINE =================
with tab_feed:
    cats = ["All"] + sorted({p["category"] for p in posts})
    pick = st.selectbox("Filter", cats)
    if "likes" not in st.session_state:
        st.session_state.likes = {p["id"]: p["likes"] for p in posts}
    if "comments" not in st.session_state:
        st.session_state.comments = {p["id"]: list(p.get("comments", [])) for p in posts}

    shown = [p for p in posts if pick == "All" or p["category"] == pick]
    for p in shown:
        with st.container(border=True):
            st.markdown(f"**{PERSONA['avatar']} {PERSONA['name']}** ✔ · `{p['icon']} {p['category']}`")
            st.write(p["caption"])
            try:
                st.image(p["image"], use_container_width=True)
            except Exception:
                st.caption(f"[image: {p['image']}]")

            # CV output
            if p.get("vision"):
                with st.expander("🔬 Computer-Vision output (Module 1)"):
                    st.json(p["vision"])

            # poll
            if p.get("poll"):
                opts = p["poll"]["options"]
                votes = p["poll"]["votes"]
                choice = st.radio("Vote:", opts, key=f"poll{p['id']}", horizontal=True)
                if st.button("Vote 🗳️", key=f"votebtn{p['id']}"):
                    votes[opts.index(choice)] += 1
                total = sum(votes) or 1
                for o, v in zip(opts, votes):
                    st.progress(v / total, text=f"{o} — {round(v/total*100)}%")

            # quiz
            if p.get("quiz"):
                opts = p["quiz"]["options"]
                ans = st.radio("Your answer:", opts, key=f"quiz{p['id']}")
                if st.button("Check ✅", key=f"quizbtn{p['id']}"):
                    if opts.index(ans) == p["quiz"]["answer"]:
                        st.success("✅ Correct! 🎉")
                    else:
                        st.error(f"❌ Not quite — it's **{opts[p['quiz']['answer']]}**")

            st.caption(" ".join(p["hashtags"]))

            c1, c2 = st.columns([1, 4])
            with c1:
                if st.button(f"❤️ {st.session_state.likes[p['id']]:,}", key=f"like{p['id']}"):
                    st.session_state.likes[p["id"]] += 1
                    st.rerun()
            with c2:
                st.download_button("⬇️ Image", data=open(p["image"], "rb").read()
                                   if __import__("os").path.exists(p["image"]) else b"",
                                   file_name=f"post_{p['id']}.png", key=f"dl{p['id']}")

            # comments
            for c in st.session_state.comments[p["id"]]:
                who = f"{PERSONA['avatar']} {PERSONA['name']}" if c.get("bot") else f"👤 {c['name']}"
                st.markdown(f"> **{who}** {c['text']}")

            with st.form(key=f"cf{p['id']}", clear_on_submit=True):
                cc1, cc2 = st.columns([1, 3])
                name = cc1.text_input("Name", key=f"nm{p['id']}")
                text = cc2.text_input("Comment (mention your team!)", key=f"tx{p['id']}")
                if st.form_submit_button("Post 💬") and name and text:
                    st.session_state.comments[p["id"]].append({"name": name, "text": text, "bot": False})
                    mem = get_memory()
                    prof = mem.remember(name, last_comment=text)
                    reply = get_text_generator().personalized_reply(prof, text)
                    st.session_state.comments[p["id"]].append({"name": PERSONA["name"], "text": reply, "bot": True})
                    st.rerun()

# ================= ANALYTICS =================
with tab_analytics:
    likes = st.session_state.get("likes", {p["id"]: p["likes"] for p in posts})
    total_likes = sum(likes.values())
    df = pd.DataFrame([{"category": p["category"], "likes": likes[p["id"]]} for p in posts])
    by_cat = df.groupby("category")["likes"].sum().sort_values(ascending=False)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total likes", f"{total_likes:,}")
    m2.metric("Posts", len(posts))
    m3.metric("Followers", f"{1_240_000 + total_likes % 5000:,}")
    m4.metric("Avg engagement", f"{total_likes/len(posts)/9800*100:.1f}%")
    st.subheader("Likes by content category")
    st.bar_chart(by_cat)
    st.subheader("Posts per category")
    st.bar_chart(df.groupby("category").size())

# ================= IMAGE REPORT =================
with tab_report:
    st.caption("Stage-1 deliverable — Module 1 (YOLO) + Module 2 (BLIP) over your input images.")
    if config.REPORT_JSON.exists():
        rep = json.loads(config.REPORT_JSON.read_text(encoding="utf-8"))
        if rep:
            st.dataframe(pd.json_normalize(rep), use_container_width=True)
        else:
            st.info("Report is empty — add images to images/<type>/ and re-run generate_posts.py.")
    else:
        st.info("No report yet. Run generate_posts.py with images in images/<type>/.")

# ================= MEMORY =================
with tab_memory:
    st.caption("Advanced Challenge — the actor remembers followers and personalises replies.")
    mem = get_memory()
    users = mem.list()
    if users:
        st.dataframe(pd.DataFrame(users), use_container_width=True)
        if st.button("🧹 Clear memory"):
            mem.clear(); st.rerun()
    else:
        st.info("No followers remembered yet. Comment on a post (mention your team!).")
