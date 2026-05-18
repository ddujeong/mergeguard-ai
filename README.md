# MergeGuard AI

MergeGuard AI는 GitHub PR 및 로컬 diff 기반 변경 사항과
협업 상태를 함께 분석하여
협업 과정에서 발생할 수 있는 충돌 위험과
영향 범위를 사전에 분석하는 것을 목표로 한다.

---

## 기술 스택

### Backend
- FastAPI
- Pydantic

### Frontend
- Next.js
- Tailwind CSS
- ReactMarkdown

### External API
- GitHub REST API
- Gemini API

### Dev Tools
- Swagger UI

### AI / LLM
- Gemini 3 Flash Preview
- Gemini 3.1 Flash Lite (Fallback)

### Static Analysis
- Tree-sitter

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

### 5. AI Merge Strategy
- 위험도 기반 Merge 전략 추천
- Rebase 필요 여부 판단
- 수동 리뷰 필요 여부 분석
- 협업 우선순위 및 체크 포인트 제공

### 6. 사전 위험 분석
- PR 생성 전 위험도 분석
- Merge 이전 협업 위험 사전 탐지
- 로컬 git diff 및 patch(.patch/.diff) 파일 기반 사전 위험 분석 지원

### 7. AST 기반 코드 구조 및 영향 범위 분석
- Tree-sitter 기반 Java AST 분석
- 변경 클래스 및 메서드 추출
- 메서드 호출 관계 분석
- 영향 범위(Call Chain) 분석
- 보안 민감 메서드 탐지
- AST 기반 메서드 위험도 계산
- 영향 범위 트리(Impact Tree) 시각화
- GitHub PR 변경 파일의 전체 Java 소스 기반 AST 분석
- 클래스/메서드 단위 Call Graph 분석
- 클래스 간 메서드 호출 흐름 분석
- 객체 타입 추론 기반 호출 대상 클래스 식별
- Controller → Service → Provider 형태의 연쇄 영향 범위 추적

### 8. Ripple Effect 분석
- 호출 체인 기반 영향 범위 점수 계산
- 최대 호출 깊이 분석
- 보안 관련 호출 비율 기반 위험도 계산
- LOW / MEDIUM / HIGH 단계 제공

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
- [x] AI Merge Strategy 생성
- [x] 협업 위험 Alert UI 추가
- [x] Diff Preview Dashboard 구현
- [x] 로컬 git diff 기반 사전 위험 분석 기능 추가
- [x] Tree-sitter 기반 AST 구조 분석
- [x] 메서드 호출 관계 분석
- [x] AST 기반 메서드 위험도 계산
- [x] 영향 범위(Call Chain) 분석
- [x] Impact Tree UI 시각화
- [x] 보안 민감 메서드 탐지
- [x] 전체 Java 소스 기반 AST 분석
- [x] 클래스 간 메서드 호출 흐름 분석
- [x] 객체 타입 추론 기반 호출 대상 클래스 식별

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
- 로컬 git diff 기반 사전 위험 분석 지원
- PR 생성 전 Merge 위험도 분석 기능 제공
- 위험도 기반 Merge 전략 추천
- Rebase 필요 여부 자동 분석
- AUTH/DB 변경 기반 협업 우선순위 분석
- Tree-sitter 기반 AST 구조 분석
- 변경 클래스 및 메서드 단위 영향 범위 추출
- Tree-sitter 기반 메서드 호출 관계 분석
- 보안 민감 메서드 탐지
- 메서드 단위 위험도 계산
- AST 기반 추가 위험 점수 반영
- 메서드 호출 체인(Call Chain) 분석
- 영향 범위(Impact Chain) 분석
- 객체 타입 추론 기반 Impact Tree 분석
- GitHub PR 변경 파일의 전체 Java 소스 기반 AST 분석
- 클래스/메서드 단위 Call Graph 분석
- Controller → Service → Provider 형태의 호출 체인 추적
- Impact Tree 기반 연쇄 호출 흐름 시각화

---

## 시스템 흐름

GitHub PR URL 또는 로컬 diff(.patch) 파일 입력
→ GitHub API 및 diff parser 기반 변경 사항 수집
→ 위험 파일 / 전체 Java 소스 기반 AST 구조 / 호출 체인 / 변경 규모 분석
→ 협업 위험도 계산
→ 열린 PR 충돌 여부 분석
→ Gemini 기반 AI 코드 리뷰 생성
→ AI Merge Strategy 생성
→ Dashboard UI 출력

---

## 프로젝트 목표

기존 코드 리뷰 시스템은 코드 품질 중심으로 동작하며,
협업 과정에서 발생하는 충돌 위험이나 브랜치 최신화 문제를 충분히 분석하지 못한다.

MergeGuard AI는 GitHub PR 및 로컬 diff 기반 변경 사항과
협업 상태를 함께 분석하여:

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

특히 PR 생성 이후의 사후 리뷰가 아닌,
개발 단계에서 협업 위험을 사전에 예방하는 방향을 목표로 하였다.

## 차별점

기존 AI 코드 리뷰 시스템은
코드 품질 및 버그 탐지 중심으로 동작하는 경우가 많다.

반면 MergeGuard AI는:

- 협업 충돌 가능성
- 공통 변경 파일
- 위험 키워드 기반 영향 범위
- Merge 이전 사전 위험 분석
- Tree-sitter 기반 AST 구조 분석을 통한 클래스 및 메서드 단위 영향 범위 분석
- 메서드 호출 관계 기반 영향 범위 분석
- AST 기반 보안 민감 메서드 탐지
- Impact Tree 기반 호출 흐름 시각화
- 전체 Java 소스 기반 AST 분석을 통해 클래스 간 호출 흐름을 추적하고,
  Controller → Service → Provider 형태의 연쇄 영향 범위를 시각화

등 협업 관점의 위험 요소를 함께 분석한다.

또한 GitHub PR 기반 분석뿐 아니라,
로컬 git diff(.patch) 기반 사전 분석 기능을 통해
PR 생성 이전 단계에서도 위험도를 점검할 수 있도록 설계하였다.

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

- PR #3: AST 호출 분석 테스트
  - AuthService.java
  - validateInput() 호출 추가

MergeGuard AI는 `login()`에서 `validateInput()`을 호출하는 관계를 분석하고,
보안 민감 메서드 및 메서드 단위 위험도를 함께 탐지하였다.

- PR #4: 인증 흐름 호출 체인 테스트
  - login()
  - validateInput()
  - checkPassword()
  - issueToken()
  - findUser()

MergeGuard AI는 login() 메서드를 기준으로
호출되는 메서드 체인을 분석하고,
영향 범위 및 보안 민감 메서드를 함께 탐지하였다.

