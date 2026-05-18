# MergeGuard AI

GitHub PR의 코드 변경 사항과 협업 충돌 위험을 분석하여 merge 안정성을 높이는 AI 기반 PR 리뷰 시스템입니다.

---

## 기술 스택

### Backend
- FastAPI

### Frontend
- Next.js
- Tailwind CSS

### External API
- GitHub REST API
- Gemini API

## 인증 방식

GitHub API Rate Limit 문제를 해결하기 위해
Personal Access Token 기반 인증 요청을 적용하였다.

---

## 핵심 기능

### 1. GitHub PR 분석
- PR 메타데이터 조회
- 변경 파일 및 Diff 수집

### 2. 협업 위험 분석
- 위험 키워드 기반 분석
- 공통 영향 파일 탐지
- 위험 점수 계산

### 3. 충돌 가능성 탐지
- 열린 PR 목록 조회
- 변경 파일 중복 여부 분석

### 4. AI 코드 리뷰
- Gemini 기반 코드 리뷰 생성
- Issues / Suggestions 구조화
- Markdown 렌더링 지원

### 5. AI Merge Guide
- 위험도 기반 Merge 전략 제안
- 협업 시 주의사항 안내
- Merge 전 체크 포인트 제공

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
- [x] Merge Risk Progress Bar 시각화
- [x] 위험 키워드 배지 표시
- [x] AI Merge Guide 생성
- [x] 협업 위험 Alert UI 추가
- [x] Diff Preview Dashboard 구현

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
- 위험 점수 기반 Progress Bar 표시
- 감지된 위험 키워드 기반 Badge UI 제공
- 변경 파일 기반 Diff Preview Dashboard 제공
- 협업 위험 Alert 메시지 제공
- AI Merge 전략 생성

---

## 시스템 흐름

GitHub PR URL 입력
→ GitHub API 기반 PR 및 Diff 수집
→ 위험 파일 및 변경 규모 분석
→ 협업 위험도 계산
→ 열린 PR 충돌 여부 분석
→ Gemini 기반 AI 코드 리뷰 생성
→ AI Merge Guide 생성
→ Dashboard UI 출력

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

## 프로젝트 배경

최근 AI 기반 코드 생성 도구와 바이브 코딩 환경의 발전으로
코드 작성 자체의 진입장벽은 크게 낮아졌다.

하지만 실제 협업 환경에서는:

- PR 충돌
- 브랜치 최신화 누락
- 영향 범위 파악 어려움
- Merge 안정성 문제

등의 협업 이슈는 여전히 개발자의 부담으로 남아있다.

MergeGuard AI는 이러한 협업 과정의 위험 요소를 사전에 분석하고,
안전한 Merge를 지원하기 위해 개발되었다.

## 테스트 시나리오

테스트용 Spring Boot 레포지토리에서 두 개의 PR을 생성하여
동일 파일 수정으로 인한 협업 충돌 상황을 재현하였다.

- PR #1: JWT 인증 로직 개선
  - JwtTokenProvider.java
  - SecurityConfig.java

- PR #2: 로그인 검증 로직 추가
  - JwtTokenProvider.java
  - AuthService.java

MergeGuard AI는 두 PR이 공통으로 수정한 `JwtTokenProvider.java`를 감지하고,
협업 충돌 가능성이 있는 PR로 분류하였다.