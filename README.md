# MergeGuard AI

GitHub PR의 코드 변경 사항과 협업 충돌 위험을 분석하여 merge 안정성을 높이는 AI 기반 PR 리뷰 시스템입니다.

---

## 기술 스택

### Backend
- FastAPI

### Frontend
- Next.js

### External API
- GitHub REST API

### LLM
- Gemini API

---

## 현재 진행 상황

- [x] FastAPI 서버 초기 세팅
- [x] Health Check API 구현
- [x] GitHub PR URL 파싱
- [x] GitHub PR 메타데이터 조회
- [x] PR 변경 파일 및 Diff 수집
- [x] 협업 충돌 위험 분석
- [ ] LLM 기반 코드 리뷰
- [ ] Frontend UI 구현

---

## 구현 완료 기능

- GitHub PR URL 분석
- GitHub Pull Request 정보 조회
- PR 변경 파일 분석
- Diff Patch 수집
- Swagger API 테스트 완료
- 위험 키워드 기반 협업 리스크 분석
- 위험 파일 탐지 및 위험도 계산

---

## 프로젝트 목표

기존 코드 리뷰 시스템은 코드 품질 중심으로 동작하며,
협업 과정에서 발생하는 충돌 위험이나 브랜치 최신화 문제를 충분히 분석하지 못한다.

MergeGuard AI는 GitHub PR의 변경 사항과 협업 상태를 함께 분석하여:

- 최신 브랜치 미반영 감지
- 충돌 가능 파일 분석
- 위험도 계산
- AI 기반 코드 리뷰
- Merge 가이드 제공

기능을 목표로 한다.