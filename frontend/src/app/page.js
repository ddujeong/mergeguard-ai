"use client";

import { useState } from "react";

import { analyzeDiffApi, analyzePrApi } from "@/api/reviewApi";

import ReactMarkdown from "react-markdown";

const getRiskBadgeStyle = (level) => {

  if (level === "HIGH") {
    return "bg-red-100 text-red-700 border-red-300";
  }

  if (level === "MEDIUM") {
    return "bg-yellow-100 text-yellow-700 border-yellow-300";
  }

  return "bg-green-100 text-green-700 border-green-300";
};

export default function HomePage() {

  const [prUrl, setPrUrl] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [mode, setMode] = useState("pr");
  const [diffText, setDiffText] = useState("");

  const mergeGuideItems =
    result?.merge_guide?.merge_strategy?.flatMap((item) =>
      item.split(/\n\d+\.\s/g).filter(Boolean)
    ) || [];
  const groupedImpactAnalysis =
    result?.deep_impact_analysis?.reduce((acc, chain) => {
      const root = chain[0];

      if (!root) return acc;

      const rootKey = `${root.class_name}.${root.method}`;

      if (!acc[rootKey]) {
        acc[rootKey] = {
          root,
          children: new Map(),
        };
      }

      chain.slice(1).forEach((method) => {
        const childKey = `${method.class_name}.${method.method}`;
        acc[rootKey].children.set(childKey, method);
      });

      return acc;
    }, {}) || {};
  const handleAnalyze = async () => {
    try {
      setLoading(true);
      setResult(null);

      const response = await analyzePrApi(prUrl);
      setResult(response);
    } catch (error) {
      console.error(error);
      alert("분석 실패");
    } finally {
      setLoading(false);
    }
  };
  const handleAnalyzeDiff = async () => {
    try {

      setLoading(true);

      setResult(null);

      const response = await analyzeDiffApi(diffText);

      setResult(response);

    } catch (error) {

      console.error(error);

      alert("Diff 분석 실패");

    } finally {

      setLoading(false);

    }
  };
  const handleDiffFileUpload = async (e) => {
    const file = e.target.files?.[0];

    if (!file) return;

    const text = await file.text();

    setDiffText(text);
  };

  return (
    <main className="min-h-screen bg-gray-100 px-6 p-10 text-black">

      <div className="w-full rounded-xl bg-white p-8 shadow">

        <h1 className="mb-6 text-3xl font-bold">
          MergeGuard AI
        </h1>
        <div className="mb-6 flex gap-3">

          <button
            onClick={() => setMode("pr")}
            className={
              mode === "pr"
                ? "rounded-lg bg-black px-5 py-2 text-white"
                : "rounded-lg bg-gray-200 px-5 py-2 text-gray-700"
            }
          >
            GitHub PR 분석
          </button>

          <button
            onClick={() => setMode("diff")}
            className={
              mode === "diff"
                ? "rounded-lg bg-indigo-600 px-5 py-2 text-white"
                : "rounded-lg bg-gray-200 px-5 py-2 text-gray-700"
            }
          >
            로컬 Diff 분석
          </button>

        </div>
        {mode === "pr" && (

          <div className="flex gap-3">

            <input
              type="text"
              value={prUrl}
              onChange={(e) => setPrUrl(e.target.value)}
              placeholder="GitHub PR URL 입력"
              className="flex-1 rounded-lg border p-3 text-black"
            />

            <button
              onClick={handleAnalyze}
              className="rounded-lg bg-black px-6 py-3 text-white"
            >
              분석하기
            </button>

          </div>

        )}
        {mode === "diff" && (

          <div className="space-y-4">
            <div className="rounded-2xl border border-dashed border-gray-300 bg-gray-50 p-5">
              <p className="mb-2 font-semibold">
                Diff 파일 업로드
              </p>

              <p className="mb-3 text-sm text-gray-500">
                터미널에서 <code className="rounded bg-white px-1">git diff &gt; changes.patch</code> 실행 후 생성된 파일을 업로드할 수 있습니다.
              </p>

              <input
                type="file"
                accept=".diff,.patch,.txt"
                onChange={handleDiffFileUpload}
                className="block w-full text-sm text-gray-700"
              />
            </div>
            <textarea
              value={diffText}
              onChange={(e) => setDiffText(e.target.value)}
              placeholder="git diff 결과를 붙여넣거나, 위에서 .patch/.diff 파일을 업로드하세요."
              className="h-72 w-full rounded-lg border p-4 font-mono text-sm text-black"
            />

            <button
              onClick={handleAnalyzeDiff}
              className="rounded-lg bg-indigo-600 px-6 py-3 text-white"
            >
              로컬 Diff 사전 분석
            </button>

          </div>

        )}
        {loading && (
          <div className="mt-8 rounded-2xl border bg-white p-6 text-black shadow-sm">
            <div className="flex items-center gap-4">
              <div className="h-6 w-6 animate-spin rounded-full border-4 border-gray-300 border-t-black" />

              <div>
                <p className="font-bold">
                  PR을 분석하고 있습니다
                </p>
                <p className="mt-1 text-sm text-gray-500">
                  Diff 수집, 협업 위험 분석, AI 코드 리뷰를 순차적으로 진행 중입니다.
                </p>
              </div>
            </div>
          </div>
        )}

        {result && (

          <div className="mt-8 space-y-8">
            <div className="grid gap-4 md:grid-cols-4">

              <div className="rounded-2xl border bg-white p-5 shadow-sm">
                <p className="text-sm text-gray-500">Repository</p>
                <p className="mt-1 font-bold">{result.repository}</p>
              </div>

              <div className="rounded-2xl border bg-white p-5 shadow-sm">
                <p className="text-sm text-gray-500">Author</p>
                <p className="mt-1 font-bold">{result.author}</p>
              </div>

              <div className="rounded-2xl border bg-white p-5 shadow-sm">
                <p className="text-sm text-gray-500">Changed Files</p>
                <p className="mt-1 text-2xl font-bold">{result.changed_files}</p>
              </div>

              <div className="rounded-2xl border bg-white p-5 shadow-sm">
                <p className="text-sm text-gray-500">Commits</p>
                <p className="mt-1 text-2xl font-bold">{result.commits}</p>
              </div>

            </div>
            {result.risk_analysis?.detected_keywords?.length > 0 && (

              <div className="rounded-2xl border border-orange-200 bg-orange-50 p-5 text-orange-800 shadow-sm">

                <div className="flex items-start gap-3">

                  <div className="mt-1 text-xl">
                    ⚠️
                  </div>

                  <div>

                    <h2 className="mb-2 text-lg font-bold">
                      협업 주의 알림
                    </h2>

                    <p className="leading-relaxed">
                      현재 PR은{" "}
                      <span className="font-semibold">
                        {result.risk_analysis?.detected_keywords?.join(", ")}
                      </span>
                      {" "}관련 변경을 포함하고 있습니다.
                      팀원 작업 및 최신 브랜치 상태를 확인한 뒤 merge 하는 것을 권장합니다.
                    </p>

                  </div>

                </div>

              </div>
            )}
            <div className="rounded-2xl border bg-white p-6 shadow-sm">

              <div className="mb-4 flex items-center justify-between">

                <h2 className="text-xl font-bold">
                  위험도 분석
                </h2>

                <span
                  className={`rounded-full border px-4 py-1 text-sm font-semibold ${getRiskBadgeStyle(
                    result.risk_analysis?.risk_level
                  )}`}
                >
                  {result.risk_analysis?.risk_level}
                </span>

              </div>

              <p className="mb-2 text-lg">
                위험 점수:
                {" "}
                <span className="font-bold">
                  {result.risk_analysis?.risk_score}
                </span>
              </p>
              <div className="mt-4">

                <div className="mb-2 flex justify-between text-sm">
                  <span>병합 위험도</span>
                  <span>{result.risk_analysis?.risk_score}%</span>
                </div>

                <div className="h-3 overflow-hidden rounded-full bg-gray-200">

                  <div
                    className={
                      result.risk_analysis?.risk_level === "HIGH"
                        ? "h-full bg-red-500"
                        : result.risk_analysis?.risk_level === "MEDIUM"
                          ? "h-full bg-yellow-500"
                          : "h-full bg-green-500"
                    }
                    style={{
                      width: `${result.risk_analysis?.risk_score}%`,
                    }}
                  />

                </div>

              </div>
              {result.risk_analysis?.detected_keywords?.length > 0 && (
                <div className="mt-4">
                  <h3 className="mb-2 font-semibold">
                    감지된 위험 키워드
                  </h3>

                  <div className="flex flex-wrap gap-2">
                    {result.risk_analysis?.detected_keywords?.map((keyword) => (
                      <span
                        key={keyword}
                        className="rounded-full bg-orange-100 px-3 py-1 text-sm font-semibold text-orange-700"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              <div className="mt-4">

                <h3 className="mb-2 font-semibold">
                  위험 파일
                </h3>

                <div className="flex flex-wrap gap-2">

                  {result.risk_analysis?.risky_files?.map((file) => (
                    <span
                      key={file}
                      className="rounded-lg bg-gray-100 px-3 py-1 text-sm"
                    >
                      {file}
                    </span>
                  ))}

                </div>

              </div>

            </div>
            {result.ast_risk_analysis && (
              <div className="mt-4 rounded-xl border bg-orange-50 p-4">

                <div className="flex items-center justify-between">

                  <span className="font-semibold text-orange-700">
                    AST 기반 추가 위험 점수
                  </span>

                  <span className="rounded-full bg-orange-100 px-3 py-1 text-sm font-bold text-orange-700">
                    +{result.ast_risk_analysis.ast_risk_score}
                  </span>

                </div>

              </div>
            )}
            <div className="rounded-2xl border border-indigo-100 bg-indigo-50 p-6 text-black shadow-sm">

              <div className="mb-4 flex items-center justify-between">

                <h2 className="text-xl font-bold text-indigo-700">
                  PR 복잡도 분석
                </h2>

                <span className="rounded-full bg-white px-4 py-1 text-sm font-bold">
                  {result.complexity_analysis?.complexity_level}
                </span>

              </div>

              <div className="grid gap-4 md:grid-cols-3">

                <div className="rounded-xl bg-white p-4">
                  <p className="text-sm text-gray-500">
                    복잡도 점수
                  </p>
                  <p className="mt-2 text-2xl font-bold">
                    {result.complexity_analysis?.complexity_score}
                  </p>
                </div>

                <div className="rounded-xl bg-white p-4">
                  <p className="text-sm text-gray-500">
                    추가된 코드
                  </p>
                  <p className="mt-2 text-2xl font-bold text-green-600">
                    +{result.complexity_analysis.total_additions}
                  </p>
                </div>

                <div className="rounded-xl bg-white p-4">
                  <p className="text-sm text-gray-500">
                    삭제 된 코드
                  </p>
                  <p className="mt-2 text-2xl font-bold text-red-600">
                    -{result.complexity_analysis?.total_deletions}
                  </p>
                </div>

              </div>

            </div>
            {result.ast_analysis && (
              <section className="rounded-2xl border bg-white p-5 shadow-sm">

                <div className="mb-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold">
                    코드 구조 분석
                  </h2>

                  <span className="rounded-full bg-indigo-100 px-3 py-1 text-sm font-semibold text-indigo-700">
                    AST
                  </span>
                </div>

                <div className="grid gap-4 md:grid-cols-3">

                  <div className="rounded-xl border bg-gray-50 p-4">
                    <p className="mb-3 text-sm font-semibold text-gray-500">
                      변경 클래스
                    </p>

                    <div className="flex flex-wrap gap-2">

                      {result.ast_analysis.classes?.length > 0 ? (
                        result.ast_analysis.classes.map(
                          (item, index) => (
                            <span
                              key={index}
                              className="rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-700"
                            >
                              {item}
                            </span>
                          )
                        )
                      ) : (
                        <p className="text-sm text-gray-400">
                          감지된 클래스 없음
                        </p>
                      )}

                    </div>
                  </div>

                  <div className="rounded-xl border bg-gray-50 p-4">
                    <p className="mb-3 text-sm font-semibold text-gray-500">
                      변경 메서드
                    </p>

                    <div className="flex flex-wrap gap-2">

                      {result.ast_analysis.methods?.length > 0 ? (
                        result.ast_analysis.methods.map(
                          (item, index) => (
                            <span
                              key={index}
                              className="rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-700"
                            >
                              {item}()
                            </span>
                          )
                        )
                      ) : (
                        <p className="text-sm text-gray-400">
                          감지된 메서드 없음
                        </p>
                      )}

                    </div>
                  </div>
                  <div className="rounded-xl border bg-gray-50 p-4">
                    <p className="mb-3 text-sm font-semibold text-gray-500">
                      호출 메서드
                    </p>

                    <div className="flex flex-wrap gap-2">
                      {result.ast_analysis.method_calls?.length > 0 ? (
                        result.ast_analysis.method_calls.map((item, index) => (
                          <span
                            key={index}
                            className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700"
                          >
                            {item}()
                          </span>
                        ))
                      ) : (
                        <p className="text-sm text-gray-400">
                          감지된 호출 없음
                        </p>
                      )}
                    </div>
                  </div>

                </div>
              </section>
            )}
            {result.ast_analysis.call_relations?.length > 0 && (
              <section className="rounded-2xl border bg-white p-5 shadow-sm">

                <div className="mb-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold">
                    메서드 호출 관계 분석
                  </h2>

                  <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-700">
                    CALL GRAPH
                  </span>
                </div>

                <div className="space-y-3">

                  {result.ast_analysis.call_relations.map(
                    (relation, index) => (

                      <div
                        key={index}
                        className="rounded-xl border bg-gray-50 p-4"
                      >

                        <span className="font-semibold text-indigo-600">
                          {relation.caller}()
                        </span>

                        <span className="mx-2 text-gray-400">
                          →
                        </span>

                        <span className="font-semibold text-emerald-600">
                          {relation.object_class
                            ? `${relation.object_class}.${relation.callee}()`
                            : `${relation.callee}()`}
                        </span>

                      </div>
                    )
                  )}

                </div>
              </section>
            )}
            {Object.keys(groupedImpactAnalysis).length > 0 && (
              <section className="rounded-2xl border bg-white p-5 shadow-sm">
                <div className="mb-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold">영향 범위 분석</h2>
                  <span className="rounded-full bg-cyan-100 px-3 py-1 text-sm font-semibold text-cyan-700">
                    IMPACT TREE
                  </span>
                </div>

                <div className="space-y-4">
                  {Object.entries(groupedImpactAnalysis).map(([rootKey, group]) => (
                    <div key={rootKey} className="rounded-xl border bg-gray-50 p-4">
                      <div className="font-bold text-cyan-700">
                        ● {group.root.class_name}.{group.root.method}()
                      </div>

                      <div className="mt-2 space-y-1 pl-6">
                        {[...group.children.entries()].map(([childKey, child]) => (
                          <div key={childKey} className="font-semibold text-cyan-700">
                            └─ {child.class_name}.{child.method}()
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>

                <p className="mt-4 text-sm text-cyan-700">
                  변경 메서드의 호출 체인을 기반으로 연쇄 영향 범위를 분석합니다.
                </p>
              </section>
            )}
            {result.ast_analysis?.undefined_calls?.length > 0 && (
              <section className="rounded-2xl border border-red-200 bg-red-50 p-5 shadow-sm">

                <div className="mb-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold text-red-700">
                    미정의 메서드 탐지
                  </h2>

                  <span className="rounded-full bg-red-100 px-3 py-1 text-sm font-semibold text-red-700">
                    STATIC CHECK
                  </span>
                </div>

                <div className="space-y-3">
                  {result.ast_analysis.undefined_calls.map((method, index) => (
                    <div
                      key={index}
                      className="rounded-xl border bg-white p-4 text-red-700"
                    >
                      ⚠ {method}() 호출은 감지되었지만, 현재 분석 범위 내 구현 여부를 확인할 수 없습니다.
                    </div>
                  ))}
                </div>

              </section>
            )}
            {result.ast_analysis?.sensitive_methods?.length > 0 && (
              <section className="rounded-2xl border border-orange-200 bg-orange-50 p-5 shadow-sm">

                <div className="mb-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold text-orange-700">
                    보안 민감 메서드 탐지
                  </h2>

                  <span className="rounded-full bg-orange-100 px-3 py-1 text-sm font-semibold text-orange-700">
                    SECURITY CHECK
                  </span>
                </div>

                <div className="flex flex-wrap gap-2">
                  {result.ast_analysis.sensitive_methods.map((method, index) => (
                    <span
                      key={index}
                      className="rounded-full bg-white px-3 py-1 text-sm font-semibold text-orange-700"
                    >
                      ⚠ {method}()
                    </span>
                  ))}
                </div>

                <p className="mt-3 text-sm text-orange-700">
                  인증, 토큰, 비밀번호, 삭제, 결제 등 보안 영향이 큰 메서드는 리뷰 우선순위를 높게 판단합니다.
                </p>

              </section>
            )}
            {result.ast_analysis?.method_risks?.length > 0 && (
              <section className="rounded-2xl border bg-white p-5 shadow-sm">

                <div className="mb-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold">
                    메서드 위험도 분석
                  </h2>

                  <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-700">
                    RISK SCORE
                  </span>
                </div>

                <div className="space-y-3">

                  {result.ast_analysis.method_risks.map(
                    (item, index) => (

                      <div
                        key={index}
                        className="flex items-center justify-between rounded-xl border p-4"
                      >

                        <span className="font-semibold">
                          {item.method}()
                        </span>

                        <span
                          className={`rounded-full px-3 py-1 text-sm font-bold
              ${item.risk_level === "HIGH"
                              ? "bg-red-100 text-red-700"
                              : item.risk_level === "MEDIUM"
                                ? "bg-yellow-100 text-yellow-700"
                                : "bg-green-100 text-green-700"
                            }`}
                        >
                          {item.risk_level}
                        </span>

                      </div>
                    )
                  )}

                </div>
              </section>
            )}
            <div className="rounded-lg border bg-white p-5 text-black">
              <h2 className="mb-3 text-xl font-bold">
                협업 충돌 분석
              </h2>

              <p className="mb-3">
                겹치는 열린 PR 수:{" "}
                <span className="font-bold">
                  {result.conflict_analysis?.conflict_count}
                </span>
              </p>

              {result.repository === "LOCAL_DIFF" ? (
                <p className="text-gray-600">
                  로컬 Diff 분석 모드에서는 열린 PR 비교를 수행하지 않습니다.
                  PR 생성 전 변경 파일과 위험 키워드를 기준으로 사전 위험도를 분석합니다.
                </p>
              ) : result.conflict_analysis?.conflict_count === 0 ? (
                <p className="text-gray-600">
                  현재 열린 PR 기준으로 변경 파일이 겹치는 항목은 없습니다.
                </p>
              ) : (
                <div className="space-y-3">
                  {result.conflict_analysis?.conflict_prs?.map((pr) => (
                    <div
                      key={pr.pr_number}
                      className="rounded-lg border bg-gray-50 p-4"
                    >
                      <p className="font-semibold">
                        #{pr.pr_number} {pr.title}
                      </p>

                      <p className="mt-2 text-sm text-gray-700">
                        겹치는 파일
                      </p>

                      <ul className="mt-1 list-disc pl-5">
                        {pr.overlapping_files?.map((file) => (
                          <li key={file}>
                            {file}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div className="space-y-6 rounded-lg border bg-white p-5 text-black">

              <div className="rounded-2xl border border-gray-200 bg-gray-50 p-6 shadow-sm">

                <div className="mb-4 flex items-center gap-2">

                  <div className="h-3 w-3 rounded-full bg-black" />

                  <h2 className="text-xl font-bold">
                    AI 코드 리뷰 요약
                  </h2>

                </div>

                <div className="prose max-w-none text-black">
                  <ReactMarkdown>
                    {result.llm_review?.summary}
                  </ReactMarkdown>
                </div>

              </div>
              <div className="grid gap-6 lg:grid-cols-2">
                <div className="rounded-2xl border border-red-100 bg-red-50 p-6 text-black shadow-sm">
                  <h3 className="mb-4 text-lg font-bold text-red-700">
                    문제 가능성
                  </h3>

                  <div className="space-y-4">
                    {result.llm_review?.issues?.map((issue, index) => (
                      <div
                        key={index}
                        className="rounded-xl border bg-white p-4"
                      >
                        <ReactMarkdown>
                          {issue}
                        </ReactMarkdown>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="rounded-2xl border border-blue-100 bg-blue-50 p-6 text-black shadow-sm">
                  <h3 className="mb-4 text-lg font-bold text-blue-700">
                    개선 제안
                  </h3>

                  <div className="space-y-4">
                    {result.llm_review?.suggestions?.map((suggestion, index) => (
                      <div
                        key={index}
                        className="rounded-xl border bg-white p-4"
                      >
                        <ReactMarkdown>
                          {suggestion}
                        </ReactMarkdown>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

            </div>
            {result.merge_guide?.merge_strategy && (
              <div className="rounded-2xl border border-purple-100 bg-purple-50 p-6 text-black shadow-sm">
                <h2 className="mb-4 text-xl font-bold text-purple-700">
                  AI 병합 가이드
                </h2>

                <div className="space-y-3">
                  {mergeGuideItems.map((item, index) => (
                    <div
                      key={index}
                      className="rounded-xl border bg-white p-4"
                    >
                      <ReactMarkdown>
                        {item}
                      </ReactMarkdown>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        )}

      </div>

    </main>
  );
}