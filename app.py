import base64
import io
import os

import streamlit as st
from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)
from PIL import Image, ImageOps

from styles import CSS, FOOTER_HTML, HEADER_HTML

load_dotenv()

DEFAULT_MODEL = "gpt-4o-mini"
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
MAX_SIDE = 1024
NO_FACE_MESSAGE = "얼굴이 확인되지 않습니다. 정면 사진을 올려주세요."
DISCLAIMER = "※ 본 풀이는 재미·오락 목적이며 과학적·의학적 근거가 없습니다."
TOPICS = ["재물운", "연애운", "직업운", "건강운"]

SYSTEM_PROMPT = f"""당신은 전통 관상학에 정통한 관상가입니다. 사용자가 올린 얼굴 사진을 보고 '재미로 보는 오락용 관상 풀이'를 한국어로 작성하세요.

규칙:
- 긍정적이고 건설적인 톤을 유지하세요. 단정적인 예언, 인종·장애·외모 비하 등 차별적 표현을 쓰지 마세요.
- 질병 진단이나 범죄 성향에 대한 언급은 금지입니다.
- 사진에 사람 얼굴이 없거나 식별이 불가능하면 다른 말 없이 정확히 다음 문장만 출력하세요: "{NO_FACE_MESSAGE}"
- 이것은 오락용 해석이므로 분석을 거부하지 말고, 외모의 인상(생김새)에 근거한 일반적인 풀이만 하세요. 신원을 추측하지 마세요.

출력 형식 (마크다운, 이 순서와 제목을 지킬 것):
## 🔮 한 줄 총평
(한 문장)

## 👁️ 부위별 해석
- **이마**: ...
- **눈**: ...
- **눈썹**: ...
- **코**: ...
- **입**: ...
- **귀**: ...(보이지 않으면 '사진에서 확인하기 어려워요')
- **턱/얼굴형**: ...

## ⭐ 운세 요약
- 재물운: ★★★☆☆ (한 줄 설명)
- 연애운: ★★★☆☆ (한 줄 설명)
- 직업운: ★★★☆☆ (한 줄 설명)
- 건강운: ★★★☆☆ (한 줄 설명)

## 💬 조언
(한 줄)

---
{DISCLAIMER}"""


def load_api_key() -> str | None:
    """st.secrets(배포) 우선, 없으면 환경변수(.env, 로컬) 사용."""
    try:
        key = st.secrets["OPENAI_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")


def prepare_image(image_bytes: bytes) -> bytes:
    """EXIF 회전 보정, RGB 변환, 긴 변 1024px 리사이즈 후 JPEG 바이트 반환 (메모리 처리)."""
    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def build_user_prompt(gender: str, age: str, topics: list[str]) -> str:
    lines = ["이 사진의 관상을 봐주세요."]
    if gender != "선택 안 함":
        lines.append(f"성별: {gender}")
    if age != "선택 안 함":
        lines.append(f"나이대: {age}")
    if topics:
        lines.append(f"특히 다음 주제를 더 자세히 풀이해 주세요: {', '.join(topics)}")
    return "\n".join(lines)


def analyze_face(image_bytes: bytes, user_prompt: str, api_key: str) -> str:
    model = os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    data_url = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"
    client = OpenAI(api_key=api_key, timeout=60)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        max_tokens=1200,
    )
    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise ValueError("빈 응답이 반환되었습니다.")
    # 모델이 분석 자체를 거절한 경우를 대비한 안내
    refusal_hints = ("I can't", "I cannot", "I'm sorry", "죄송하지만", "도와드릴 수 없")
    if len(text) < 200 and any(h in text for h in refusal_hints):
        return (
            "모델이 이 사진의 분석을 진행하지 못했습니다. "
            "정면이 잘 보이는 다른 사진으로 다시 시도해 주세요.\n\n" + DISCLAIMER
        )
    return text


def friendly_error(e: Exception) -> str:
    if isinstance(e, AuthenticationError):
        return "API 키가 올바르지 않습니다. OPENAI_API_KEY를 확인해 주세요."
    if isinstance(e, RateLimitError):
        return "요청이 너무 많거나 사용 한도를 초과했습니다. 잠시 후 다시 시도해 주세요."
    if isinstance(e, APITimeoutError):
        return "응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요."
    if isinstance(e, APIConnectionError):
        return "네트워크 연결에 문제가 있습니다. 인터넷 연결을 확인해 주세요."
    return f"분석 중 오류가 발생했습니다: {e}"


def get_image_source():
    """업로드/카메라 탭에서 이미지를 받아 (bytes, 파일크기) 반환."""
    tab_upload, tab_camera = st.tabs(["📁 사진 업로드", "📷 카메라 촬영"])
    with tab_upload:
        uploaded = st.file_uploader(
            "얼굴 사진을 올려주세요 (JPG/PNG, 최대 5MB)", type=["jpg", "jpeg", "png"]
        )
    with tab_camera:
        camera = st.camera_input("정면을 바라보고 촬영해 주세요")

    source = camera or uploaded
    if source is None:
        return None
    data = source.getvalue()
    if len(data) > MAX_UPLOAD_BYTES:
        st.warning("이미지가 5MB를 초과합니다. 더 작은 사진을 올려주세요.")
        return None
    return data


def run_analysis(image_data: bytes, user_prompt: str):
    api_key = load_api_key()
    if not api_key:
        st.error("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일(또는 Streamlit Secrets)을 확인하세요.")
        return
    try:
        prepared = prepare_image(image_data)
    except Exception:
        st.error("이미지를 읽을 수 없습니다. 다른 사진을 올려주세요.")
        return
    with st.spinner("🔮 관상을 살피는 중입니다..."):
        try:
            st.session_state["result"] = analyze_face(prepared, user_prompt, api_key)
        except Exception as e:
            st.session_state.pop("result", None)
            st.error(friendly_error(e))


def main():
    st.set_page_config(page_title="AI 관상 분석기", page_icon="🔮", layout="centered")
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HEADER_HTML, unsafe_allow_html=True)

    image_data = get_image_source()
    if image_data:
        st.image(image_data, use_container_width=True)

    with st.expander("옵션 (선택)"):
        col1, col2 = st.columns(2)
        gender = col1.selectbox("성별", ["선택 안 함", "남성", "여성"])
        age = col2.selectbox(
            "나이대", ["선택 안 함", "10대", "20대", "30대", "40대", "50대", "60대 이상"]
        )
        topics = st.multiselect("더 궁금한 주제", TOPICS)

    user_prompt = build_user_prompt(gender, age, topics)

    col_a, col_b = st.columns(2)
    if col_a.button("관상 보기", type="primary", disabled=image_data is None, use_container_width=True):
        run_analysis(image_data, user_prompt)
    if col_b.button(
        "다시 분석", disabled=image_data is None or "result" not in st.session_state,
        use_container_width=True,
    ):
        run_analysis(image_data, user_prompt)

    result = st.session_state.get("result")
    if result:
        st.write("")
        with st.container(border=True, key="result_card"):
            st.markdown(result)
            st.download_button(
                "결과 텍스트 저장", data=result, file_name="관상_결과.txt", mime="text/plain"
            )

    st.markdown(FOOTER_HTML, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
