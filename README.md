# MergeGuard AI

GitHub PR의 코드 변경 사항과 협업 충돌 위험을 분석하여 merge 안정성을 높이는 AI 기반 PR 리뷰 시스템입니다.

---

## 기술 스택

### Backend
- FastAPI

### Frontend
- Next.js

## External API

- GitHub REST API
- Gemini API

## 인증 방식

GitHub API Rate Limit 문제를 해결하기 위해
Personal Access Token 기반 인증 요청을 적용하였다.

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
- [x] LLM 기반 코드 리뷰
- [x] Gemini 응답 JSON 구조화
- [x] Frontend UI 구현
- [x] Markdown 기반 리뷰 렌더링
- [x] 열린 PR 기반 충돌 가능성 분석
- [x] GitHub API 인증 토큰 적용

---

## 구현 완료 기능

- GitHub PR URL 분석
- GitHub Pull Request 정보 조회
- PR 변경 파일 분석
- Diff Patch 수집
- Swagger API 테스트 완료
- 위험 키워드 기반 협업 리스크 분석
- 위험 파일 탐지 및 위험도 계산
- Gemini 기반 코드 리뷰 생성
- 코드 리뷰 결과를 summary / issues / suggestions 구조로 분리
- ReactMarkdown 기반 리뷰 렌더링
- Next.js 기반 PR 분석 UI 구현
- 현재 PR과 열린 PR 간 변경 파일 중복 여부 분석
- GitHub Personal Access Token 기반 API 인증 적용
- 겹치는 파일 기준 협업 충돌 가능성 탐지

---

## 시스템 흐름

GitHub PR URL 입력
→ GitHub API 기반 PR 및 Diff 수집
→ 위험 파일 및 변경 규모 분석
→ 협업 위험도 계산
→ Gemini 기반 AI 코드 리뷰 생성
→ Frontend UI 출력

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