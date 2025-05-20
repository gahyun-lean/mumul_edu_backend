# ── 1. 베이스 이미지 선택 ───────────────────────
FROM python:3.11-slim

# ── 2. 환경변수 설정 ───────────────────────────
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# ── 3. 의존성 복사 및 설치 ─────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── 4. 애플리케이션 코드 복사 ───────────────────
COPY . .

# ── 5. 컨테이너 외부 노출 포트 설정 ───────────────
EXPOSE 8000

# ── 6. 앱 실행 명령어 ────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
