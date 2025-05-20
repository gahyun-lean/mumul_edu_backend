# Mumul Edu 백엔드

## 프로젝트 개요

- **FastAPI** 기반의 교육 플랫폼 백엔드
- **Supabase** 기반 데이터베이스 및 인증
- **Google Cloud Storage** 파일 업로드
- 서비스/레포지토리/의존성 주입/테스트/로깅/설정 등 모던 백엔드 아키텍처 적용

---

## 폴더 구조

```
app/
  core/           # 핵심 설정, 로깅, 예외, supabase 클라이언트 등
  dependencies/   # FastAPI Depends 의존성 관리
  repositories/   # DB 접근 레포지토리 (Supabase 기반)
  routers/        # FastAPI 엔드포인트(라우터)
  schemas/        # Pydantic 데이터 모델/스키마
  services/       # 비즈니스 로직 서비스 계층
  tests/
    unit/         # 단위 테스트
    integration/  # 통합 테스트(엔드포인트)
```

---

## 주요 파일/모듈 설명

- `core/config.py` : Pydantic 기반 환경 변수/설정 관리 (타입 안전성, 검증)
- `core/supabase.py` : Supabase 클라이언트 인스턴스 생성
- `core/logging.py` : 로깅 설정 및 미들웨어
- `repositories/implementations/supabase/` : 각 엔티티별 DB 접근 레포지토리
- `services/` : 각 도메인별 비즈니스 로직 (DI/비동기/테스트 용이)
- `routers/` : FastAPI 엔드포인트(RESTful API)
- `dependencies/services.py` : 서비스/레포지토리 DI 및 Depends 관리
- `tests/unit/` : 서비스/레포지토리 단위 테스트 (pytest, AsyncMock)
- `tests/integration/` : 실제 API 엔드포인트 통합 테스트

---

## 개발/운영 방법

### 1. 환경 변수 설정
- `.env` 파일에 아래 항목을 반드시 설정
```
ENVIRONMENT=development
SUPABASE_URL=...
SUPABASE_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
DIFY_API_KEY=...
GCS_BUCKET_NAME=...
FRONTEND_URL=...
JWT_SECRET=...
```

### 2. 의존성 설치
```
pip install -r requirements.txt
```

### 3. 개발 서버 실행
```
uvicorn app.main:app --reload
```

### 4. 테스트 실행
- **단위 테스트**
  ```
  pytest app/tests/unit/
  ```
- **통합 테스트**
  ```
  pytest app/tests/integration/
  ```

---

## 아키텍처/DI/테스트 전략

- **서비스/레포지토리 분리**: DB 접근과 비즈니스 로직 분리, 유지보수/테스트 용이
- **의존성 주입(DI)**: FastAPI Depends + Factories로 서비스/레포지토리 주입
- **비동기 처리**: 모든 서비스/레포지토리/외부 API 비동기 지원
- **테스트 구조화**: 단위/통합 테스트 분리, pytest 픽스처 재사용, 모킹 활용
- **환경 변수/설정**: Pydantic Settings로 타입 안전성/검증 보장
- **로깅/에러 처리**: 미들웨어 및 커스텀 예외로 일관된 로깅/에러 응답

---

## 컨벤션/기타

- 코드 스타일: [PEP8](https://www.python.org/dev/peps/pep-0008/), 타입힌트 적극 사용
- 커밋 메시지: 기능/버그/리팩토링/문서 등 prefix 사용 권장
- PR 리뷰: 테스트/문서화/코드리뷰 필수

---

## 문의/기여
- 이 저장소는 팀/오픈소스 협업을 위해 설계되었습니다.
- 궁금한 점/기여/이슈는 PR 또는 Issue로 남겨주세요.

