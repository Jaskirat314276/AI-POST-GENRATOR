import html

import streamlit as st

from few_shot import FewShotPosts
from post_generator import generate_post


LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]

LENGTH_DESCRIPTIONS = {
    "Short": "1-5 lines",
    "Medium": "6-10 lines",
    "Long": "11-15 lines",
}

LANGUAGE_DESCRIPTIONS = {
    "English": "Standard English",
    "Hinglish": "Hindi + English mix, written in English script",
}


CUSTOM_CSS = """
<style>
    #MainMenu, footer, header[data-testid="stHeader"] {visibility: hidden; height: 0;}

    @keyframes pop-in {
        0%   { opacity: 0; transform: translateY(16px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes gradient-shift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background:
            radial-gradient(ellipse 800px 600px at 15% 10%,  rgba(124, 92, 255, 0.20) 0%, transparent 60%),
            radial-gradient(ellipse 700px 500px at 85% 20%,  rgba(56, 189, 248, 0.16) 0%, transparent 60%),
            radial-gradient(ellipse 600px 500px at 50% 90%,  rgba(236, 72, 153, 0.10) 0%, transparent 60%),
            linear-gradient(180deg, #0a0b14 0%, #0e1020 100%);
        background-attachment: fixed;
        color: #f5f6fa !important;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 980px;
    }

    /* GLOBAL TEXT — force high contrast everywhere */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    p, span, div, li {
        color: #e6e8f0;
    }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }

    /* HERO — glassmorphism */
    .hero {
        position: relative;
        padding: 2.75rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 2.5rem;
        background:
            linear-gradient(135deg, rgba(124, 92, 255, 0.22) 0%, rgba(56, 189, 248, 0.12) 100%),
            rgba(20, 22, 38, 0.65);
        border: 1px solid rgba(124, 92, 255, 0.30);
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.35),
            0 30px 60px rgba(124, 92, 255, 0.18),
            inset 0 1px 0 rgba(255, 255, 255, 0.10);
    }
    .hero .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(124, 92, 255, 0.18);
        border: 1px solid rgba(124, 92, 255, 0.38);
        color: #d6cdff !important;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.4px;
        margin-bottom: 1rem;
    }
    .hero .badge .dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #7c5cff;
        box-shadow: 0 0 10px #7c5cff;
    }
    .hero h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.05;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #a5b4fc 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #b8bccd !important;
        margin: 1rem 0 0 0;
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 640px;
    }

    /* SECTION HEADINGS */
    .section-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8b91a7 !important;
        margin: 1.75rem 0 0.85rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-title::before {
        content: "";
        width: 4px; height: 16px;
        border-radius: 2px;
        background: linear-gradient(180deg, #7c5cff, #38bdf8);
    }

    /* SELECTBOXES */
    div[data-baseweb="select"] > div {
        background: rgba(20, 22, 38, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        min-height: 50px;
        transition: all 0.2s ease;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.06),
            0 4px 12px rgba(0, 0, 0, 0.20);
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(124, 92, 255, 0.45) !important;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 6px 18px rgba(124, 92, 255, 0.18);
    }
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [data-baseweb="tag"] {
        color: #f5f6fa !important;
        font-weight: 500 !important;
    }
    /* dropdown popup */
    div[data-baseweb="popover"] {
        background: rgba(20, 22, 38, 0.95) !important;
        backdrop-filter: blur(20px);
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
    }
    div[data-baseweb="popover"] li {
        color: #e6e8f0 !important;
        background: transparent !important;
    }
    div[data-baseweb="popover"] li:hover {
        background: rgba(124, 92, 255, 0.18) !important;
        color: #ffffff !important;
    }

    /* WIDGET LABELS — large and crystal clear */
    label, [data-testid="stWidgetLabel"] p, .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        margin-bottom: 0.4rem !important;
        letter-spacing: 0.1px;
    }

    /* BUTTONS — vibrant gradient with glow + 3D press */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.18s cubic-bezier(.2,.8,.2,1) !important;
        letter-spacing: 0.2px;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c5cff 0%, #5b3df0 50%, #4c2fd0 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.25) inset,
            0 -2px 0 rgba(0, 0, 0, 0.18) inset,
            0 4px 0 rgba(60, 30, 160, 0.55),
            0 8px 24px rgba(124, 92, 255, 0.45),
            0 16px 40px rgba(124, 92, 255, 0.32);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.30);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        filter: brightness(1.10);
        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.30) inset,
            0 -2px 0 rgba(0, 0, 0, 0.18) inset,
            0 6px 0 rgba(60, 30, 160, 0.55),
            0 14px 32px rgba(124, 92, 255, 0.55),
            0 24px 56px rgba(124, 92, 255, 0.42);
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(2px);
        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.18) inset,
            0 1px 0 rgba(0, 0, 0, 0.20) inset,
            0 1px 0 rgba(60, 30, 160, 0.55),
            0 2px 8px rgba(124, 92, 255, 0.30);
    }
    .stButton > button:not([kind="primary"]) {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        color: #f5f6fa !important;
        backdrop-filter: blur(10px);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 4px 12px rgba(0, 0, 0, 0.22);
    }
    .stButton > button:not([kind="primary"]):hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-1px);
    }

    /* POST CARD — glass plate with gradient border */
    .post-card {
        position: relative;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%),
            rgba(20, 22, 38, 0.55);
        backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        padding: 1.85rem 2.1rem;
        margin: 1rem 0 1.25rem 0;
        font-size: 1.05rem;
        line-height: 1.75;
        white-space: pre-wrap;
        word-wrap: break-word;
        color: #f5f6fa !important;
        animation: pop-in 0.5s cubic-bezier(.2,.8,.2,1);
        box-shadow:
            0  2px  8px rgba(0, 0, 0, 0.30),
            0 16px 40px rgba(0, 0, 0, 0.40),
            0 32px 80px rgba(124, 92, 255, 0.10),
            inset 0 1px 0 rgba(255, 255, 255, 0.10);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .post-card::before {
        content: "";
        position: absolute;
        left: 0; top: 18px; bottom: 18px;
        width: 3px;
        border-radius: 0 3px 3px 0;
        background: linear-gradient(180deg, #7c5cff 0%, #38bdf8 100%);
        box-shadow: 0 0 14px rgba(124, 92, 255, 0.55);
    }
    .post-card:hover {
        transform: translateY(-3px);
        box-shadow:
            0  4px 12px rgba(0, 0, 0, 0.36),
            0 24px 50px rgba(0, 0, 0, 0.45),
            0 40px 100px rgba(124, 92, 255, 0.18),
            inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }

    /* STAT TILES — frosted glass with gradient numbers */
    .stat-card {
        position: relative;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.02) 100%),
            rgba(20, 22, 38, 0.55);
        backdrop-filter: blur(16px);
        padding: 1.1rem 1rem;
        border-radius: 14px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.10);
        transform: perspective(900px) rotateX(3deg);
        transform-origin: center bottom;
        transition: transform 0.25s cubic-bezier(.2,.8,.2,1), box-shadow 0.25s ease;
        box-shadow:
            0  2px  6px rgba(0, 0, 0, 0.22),
            0  8px 20px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.10);
    }
    .stat-card:hover {
        transform: perspective(900px) rotateX(0deg) translateY(-4px) scale(1.03);
        border-color: rgba(124, 92, 255, 0.40);
        box-shadow:
            0 4px 14px rgba(0, 0, 0, 0.28),
            0 16px 36px rgba(124, 92, 255, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.16);
    }
    .stat-card .label {
        font-size: 0.7rem;
        color: #8b91a7 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
        font-weight: 700;
    }
    .stat-card .value {
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    /* EMPTY STATE — friendly recessed panel */
    .empty-state {
        text-align: center;
        padding: 3.5rem 1.5rem;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.05) 100%),
            rgba(20, 22, 38, 0.45);
        backdrop-filter: blur(18px);
        border-radius: 18px;
        border: 1px dashed rgba(255, 255, 255, 0.14);
        box-shadow:
            inset 0 2px 8px rgba(0, 0, 0, 0.30),
            inset 0 -1px 0 rgba(255, 255, 255, 0.05);
    }
    .empty-state .icon {
        width: 56px; height: 56px;
        margin: 0 auto 1rem auto;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(124, 92, 255, 0.30), rgba(56, 189, 248, 0.20));
        border: 1px solid rgba(124, 92, 255, 0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 800;
        color: #d6cdff;
        box-shadow: 0 8px 24px rgba(124, 92, 255, 0.30);
    }
    .empty-state .title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 0.5rem;
    }
    .empty-state .subtitle {
        color: #b8bccd !important;
        font-size: 0.97rem;
    }

    /* META CHIPS (showing what was generated) */
    .meta-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.5rem 0 0.75rem 0;
    }
    .meta-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.32rem 0.75rem;
        background: rgba(124, 92, 255, 0.14);
        border: 1px solid rgba(124, 92, 255, 0.30);
        color: #d6cdff !important;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .meta-chip .key {
        color: #8b91a7 !important;
        font-weight: 500;
    }

    /* CODE BLOCK */
    .stCode, pre, code {
        background: rgba(8, 9, 18, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #e6e8f0 !important;
        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: rgba(10, 11, 20, 0.85) !important;
        backdrop-filter: blur(24px);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    [data-testid="stSidebar"] * {
        color: #e6e8f0 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] code {
        background: rgba(124, 92, 255, 0.18) !important;
        color: #d6cdff !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.85em;
    }

    /* spinner */
    .stSpinner > div { border-top-color: #7c5cff !important; }

    /* divider */
    hr, [data-testid="stDivider"] {
        border-color: rgba(255, 255, 255, 0.08) !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent) !important;
    }

    /* alert (st.error) */
    [data-testid="stAlert"] {
        background: rgba(244, 63, 94, 0.10) !important;
        border: 1px solid rgba(244, 63, 94, 0.35) !important;
        border-radius: 12px !important;
        color: #fecaca !important;
    }
</style>
"""


def render_hero():
    st.markdown(
        """
        <div class="hero">
            <div class="badge"><span class="dot"></span> Powered by Llama 3.3 70B on Groq</div>
            <h1>LinkedIn Post Generator</h1>
            <p>Write on-brand LinkedIn posts in seconds. Pick a topic, length, and language &mdash;
            the AI studies real influencer posts on that topic and matches their writing style.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("### How it works")
        st.markdown(
            """
            1. **Pick a topic** &mdash; tags pulled from real posts
            2. **Choose a length** &mdash; short, medium, or long
            3. **Select a language** &mdash; English or Hinglish
            4. Hit **Generate** &mdash; the model uses similar past posts as style examples and writes a new one
            """
        )

        st.divider()

        st.markdown("### Tips")
        st.markdown(
            """
            - Hit **Generate** again for a different angle on the same topic
            - **Hinglish** = Hindi + English mixed, written in English letters
            - Examples come from `data/processed_posts.json` &mdash; add your own posts there to personalize the style
            """
        )

        st.divider()

        st.markdown("### Stack")
        st.markdown("Streamlit · LangChain · Groq · Llama 3.3 70B")


def render_inputs(tags):
    st.markdown('<div class="section-title">Configure your post</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        tag = st.selectbox(
            "Topic",
            options=sorted(tags),
            help="The subject of the post. The model references real LinkedIn posts tagged with this topic.",
        )
    with col2:
        length = st.selectbox(
            "Length",
            options=LENGTH_OPTIONS,
            format_func=lambda x: f"{x}  ·  {LENGTH_DESCRIPTIONS[x]}",
            index=1,
            help="How many lines the generated post should be.",
        )
    with col3:
        language = st.selectbox(
            "Language",
            options=LANGUAGE_OPTIONS,
            help="English is standard. Hinglish blends Hindi words into English-script sentences.",
        )

    return tag, length, language


def render_post(post: str, meta: tuple):
    safe = html.escape(post)
    tag, length, language = meta

    st.markdown('<div class="section-title">Generated post</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="meta-row">
            <span class="meta-chip"><span class="key">Topic</span> {html.escape(tag)}</span>
            <span class="meta-chip"><span class="key">Length</span> {html.escape(length)}</span>
            <span class="meta-chip"><span class="key">Language</span> {html.escape(language)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="post-card">{safe}</div>', unsafe_allow_html=True)

    word_count = len(post.split())
    char_count = len(post)
    line_count = len([line for line in post.splitlines() if line.strip()])

    c1, c2, c3 = st.columns(3)
    stats = [(c1, "Words", word_count), (c2, "Characters", char_count), (c3, "Lines", line_count)]
    for col, label, value in stats:
        with col:
            st.markdown(
                f'<div class="stat-card"><div class="label">{label}</div><div class="value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Copy the post</div>', unsafe_allow_html=True)
    st.code(post, language=None)


def render_empty_state():
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">+</div>
            <div class="title">No post yet</div>
            <div class="subtitle">Configure your options above and click <b>Generate post</b> to create one.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="LinkedIn Post Generator",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if "generated_post" not in st.session_state:
        st.session_state.generated_post = None
    if "last_inputs" not in st.session_state:
        st.session_state.last_inputs = None

    render_hero()
    render_sidebar()

    fs = FewShotPosts()
    tag, length, language = render_inputs(fs.get_tags())

    col_gen, col_clear, _ = st.columns([1.4, 1, 3])
    with col_gen:
        generate_clicked = st.button("Generate post", type="primary", use_container_width=True)
    with col_clear:
        if st.session_state.generated_post:
            if st.button("Clear", use_container_width=True):
                st.session_state.generated_post = None
                st.session_state.last_inputs = None
                st.rerun()

    if generate_clicked:
        with st.spinner("Writing your post..."):
            try:
                st.session_state.generated_post = generate_post(length, language, tag)
                st.session_state.last_inputs = (tag, length, language)
            except Exception as exc:
                st.session_state.generated_post = None
                st.error(f"Generation failed: {exc}")

    st.divider()

    if st.session_state.generated_post and st.session_state.last_inputs:
        render_post(st.session_state.generated_post, st.session_state.last_inputs)
    else:
        render_empty_state()


if __name__ == "__main__":
    main()
