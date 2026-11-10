CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700&display=swap');

html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not([class*="material"]) {
    font-family: 'Noto Sans KR', sans-serif;
}
.stMarkdown p, .stMarkdown li { word-break: keep-all; }
h1, h2, h3, .hero-title {
    font-family: 'Noto Serif KR', serif !important;
    letter-spacing: -0.01em;
}

.stApp {
    background:
        radial-gradient(1200px 500px at 50% -10%, rgba(212,175,55,0.12), transparent 60%),
        #0f1626;
}
.block-container { max-width: 720px; padding-top: 2.2rem; padding-bottom: 3rem; }

/* 헤더 */
.hero { text-align: center; margin-bottom: 1.4rem; }
.hero-title { font-size: 2.1rem; font-weight: 700; color: #d4af37; margin: 0; }
.hero-sub { color: #cfc6ad; margin: .4rem 0 .8rem; font-size: 1rem; }
.badge {
    display: inline-block; padding: .2rem .8rem; border-radius: 999px;
    border: 1px solid rgba(212,175,55,.6); color: #e8cf7a;
    font-size: .8rem; background: rgba(212,175,55,.08);
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] { gap: .5rem; }
.stTabs [data-baseweb="tab"] { padding: .5rem 1rem; border-radius: 8px 8px 0 0; }

/* 업로드·이미지 */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(241,234,216,.05);
    border: 1.5px dashed rgba(212,175,55,.5);
    border-radius: 14px;
}
[data-testid="stImage"] img, [data-testid="stCameraInput"] video {
    border-radius: 16px;
    border: 2px solid rgba(212,175,55,.45);
}

/* 버튼 */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px; font-weight: 700; padding: .65rem 1rem;
    border: 1px solid rgba(212,175,55,.6);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #e8cf7a, #b8932b);
    color: #1a1405; border: none; font-size: 1.05rem;
}
.stButton > button[kind="primary"]:hover { filter: brightness(1.08); }
.stButton > button:disabled { opacity: .45; }

/* 옵션 expander */
[data-testid="stExpander"] {
    background: rgba(241,234,216,.04);
    border: 1px solid rgba(241,234,216,.14); border-radius: 12px;
}

/* 결과 카드 (한지 느낌) */
.st-key-result_card {
    background: #f4ecd8; color: #2a2418;
    border: 1px solid #c9b57a; border-radius: 16px;
    box-shadow: 0 8px 28px rgba(0,0,0,.35);
    padding: .6rem .9rem;
}
.st-key-result_card * { color: #2a2418; }
.st-key-result_card h2 {
    font-size: 1.15rem; color: #7a5c0a !important;
    border-bottom: 1px solid #d8c68f; padding-bottom: .3rem; margin-top: 1.1rem;
}
.st-key-result_card h2:first-child { margin-top: .2rem; }
.st-key-result_card li strong { color: #7a5c0a; }
.st-key-result_card .stDownloadButton > button {
    background: #2a2418; color: #f4ecd8 !important; border: none;
}
.st-key-result_card .stDownloadButton > button * { color: #f4ecd8 !important; }

/* 푸터 */
.footer { text-align: center; color: #9a927c; font-size: .78rem; line-height: 1.6; margin-top: 1rem; }

/* 모바일 */
@media (max-width: 640px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1.2rem; }
    .hero-title { font-size: 1.6rem; }
    .stButton > button { font-size: .95rem; }
}
</style>
"""

HEADER_HTML = """
<div class="hero">
    <p class="hero-title">🔮 AI 관상 분석기</p>
    <p class="hero-sub">사진 한 장으로 보는 나의 얼굴 이야기</p>
    <span class="badge">재미·오락 목적 · 과학적 근거 없음</span>
</div>
"""

FOOTER_HTML = """
<div class="footer">
    🔒 사진은 서버에 저장되지 않으며, 분석을 위해 OpenAI로만 전송됩니다.<br>
    본인 또는 동의받은 사진만 사용해 주세요.
</div>
"""
