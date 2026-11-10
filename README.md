# AI 관상 분석기

얼굴 사진을 업로드하면 OpenAI Vision 모델이 관상을 풀이해 주는 Streamlit 앱 (재미·오락 목적).

## 로컬 실행

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # 이후 .env에 OPENAI_API_KEY 입력
streamlit run app.py
```

## 배포 (Streamlit Community Cloud)

GitHub에 push 후 앱을 연결하고, App settings → Secrets에 `OPENAI_API_KEY = "sk-..."`를 등록합니다. `.env`는 커밋되지 않습니다.
