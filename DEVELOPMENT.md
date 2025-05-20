# 개발 가이드 (Mumul Edu)

이 문서는 Mumul Edu 백엔드 프로젝트의 개발자들을 위한 실질적인 개발 가이드입니다.

---

## 1. 프로젝트 세팅

### 1.1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 1.2. 환경 변수 설정
- `.env` 파일을 프로젝트 루트에 생성하고, README의 예시를 참고해 값을 채워주세요.
- **중요:** 민감 정보는 절대 커밋하지 마세요.

### 1.3. 개발 서버 실행
```bash
uvicorn app.main:app --reload
```

---

## 2. 브랜치 전략 & 커밋 컨벤션

- **main**: 운영 배포용, 항상 안정 상태 유지
- **dev**: 개발 통합 브랜치
- **feature/xxx**: 기능 개발
- **fix/xxx**: 버그 수정
- **docs/xxx**: 문서/주석/README 등

**커밋 메시지 예시:**
```
feat(profile): 프로필 생성 API 추가
fix(course): 강의 생성시 instructor_id 누락 버그 수정
docs(readme): 환경 변수 설명 추가
```

---

## 3. 코드 스타일 & 컨벤션

- [PEP8](https://www.python.org/dev/peps/pep-0008/) 준수, 타입힌트 적극 사용
- 함수/클래스/변수명은 명확하게
- 서비스/레포지토리/스키마/라우터 등 역할별로 파일 분리
- 불필요한 주석/코드/테스트/임포트는 주기적으로 정리

---

## 4. 테스트 & 디버깅

### 4.1. 단위 테스트
```bash
pytest app/tests/unit/
```

### 4.2. 통합 테스트
```bash
pytest app/tests/integration/
```

### 4.3. 커버리지 측정
```bash
pytest --cov=app
```

### 4.4. 테스트 픽스처
- `app/tests/conftest.py`에 공통 픽스처 정의
- 서비스/레포지토리/클라이언트 등 재사용 가능

---

## 5. 환경 변수/설정 관리
- 모든 설정은 `app/core/config.py`의 Pydantic Settings로 관리
- 타입 안전성/검증 자동 보장
- 환경 변수 누락/오타/타입 불일치 시 앱 실행 시점에 에러 발생

---

## 6. 주요 폴더/파일 설명

- `core/` : 설정, 로깅, 예외, supabase 클라이언트 등 핵심 인프라
- `services/` : 비즈니스 로직 계층
- `repositories/` : DB 접근 계층
- `routers/` : FastAPI 엔드포인트
- `schemas/` : 데이터 모델/스키마
- `dependencies/` : DI/Depends 관리
- `tests/unit/` : 단위 테스트
- `tests/integration/` : 통합 테스트

---

## 7. 자주 하는 실수 & 주의사항

- 환경 변수 누락/오타 → 앱 실행 전 `.env` 재확인
- DB/외부 API 키 노출 금지 (절대 커밋하지 말 것)
- 테스트/개발용 데이터와 운영 데이터 분리
- 테스트 실행 전/후 데이터 정리 필요시 conftest.py 활용
- 의존성/임포트 경로 꼼꼼히 확인 (특히 파일 이동 후)

---

## 8. 협업 팁

- PR은 반드시 리뷰/테스트 후 머지
- 문서/주석/테스트도 코드와 동일하게 중요하게 다룸
- 궁금한 점/이슈는 슬랙, PR, Issue로 적극 공유

---

## 9. 기타

- FastAPI 공식 문서: https://fastapi.tiangolo.com/ko/
- Supabase 공식 문서: https://supabase.com/docs
- Google Cloud Storage: https://cloud.google.com/storage/docs
- Pydantic: https://docs.pydantic.dev/

---

**즐거운 협업과 성장의 경험이 되길 바랍니다!** 