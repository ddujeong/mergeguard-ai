"use client";

import { useState } from "react";

import { analyzePrApi } from "@/api/reviewApi";

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

  const handleAnalyze = async () => {

    try {

      setLoading(true);

      const response = await analyzePrApi(prUrl);

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert("분석 실패");

    } finally {

      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 p-10 text-black">

      <div className="mx-auto max-w-4xl rounded-xl bg-white p-8 shadow">

        <h1 className="mb-6 text-3xl font-bold">
          MergeGuard AI
        </h1>

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

        {loading && (
          <p className="mt-6">
            분석 중...
          </p>
        )}

        {result && (

          <div className="mt-8 space-y-6">
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
            <div className="rounded-2xl border bg-white p-6 shadow-sm">

              <div className="mb-4 flex items-center justify-between">

                <h2 className="text-xl font-bold">
                  위험도 분석
                </h2>

                <span
                  className={`rounded-full border px-4 py-1 text-sm font-semibold ${getRiskBadgeStyle(
                    result.risk_analysis.risk_level
                  )}`}
                >
                  {result.risk_analysis.risk_level}
                </span>

              </div>

              <p className="mb-2 text-lg">
                위험 점수:
                {" "}
                <span className="font-bold">
                  {result.risk_analysis.risk_score}
                </span>
              </p>

              <div className="mt-4">

                <h3 className="mb-2 font-semibold">
                  위험 파일
                </h3>

                <div className="flex flex-wrap gap-2">

                  {result.risk_analysis.risky_files.map((file) => (
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
            <div className="rounded-lg border bg-white p-5 text-black">
              <h2 className="mb-3 text-xl font-bold">
                협업 충돌 분석
              </h2>

              <p className="mb-3">
                겹치는 열린 PR 수:{" "}
                <span className="font-bold">
                  {result.conflict_analysis.conflict_count}
                </span>
              </p>

              {result.conflict_analysis.conflict_count === 0 ? (
                <p className="text-gray-600">
                  현재 열린 PR 기준으로 변경 파일이 겹치는 항목은 없습니다.
                </p>
              ) : (
                <div className="space-y-3">
                  {result.conflict_analysis.conflict_prs.map((pr) => (
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
                        {pr.overlapping_files.map((file) => (
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
            <div className="rounded-lg border bg-white p-5 text-black">

              <h2 className="mb-3 text-xl font-bold">
                AI 코드 리뷰
              </h2>

              <div className="mb-4 prose max-w-none">
                <ReactMarkdown>
                  {result.llm_review.summary}
                </ReactMarkdown>
              </div>

              <div className="mb-4">

                <h3 className="font-semibold">
                  Issues
                </h3>

                <ul className="list-disc pl-5">

                  {result.llm_review.issues.map((issue, index) => (
                    <li key={index}>
                      <ReactMarkdown>
                        {issue}
                      </ReactMarkdown>
                    </li>
                  ))}

                </ul>

              </div>

              <div>

                <h3 className="font-semibold">
                  Suggestions
                </h3>

                <ul className="list-disc pl-5">

                  {result.llm_review.suggestions.map((suggestion, index) => (
                    <li key={index}>
                      <ReactMarkdown>
                        {suggestion}
                      </ReactMarkdown>
                    </li>
                  ))}

                </ul>

              </div>

            </div>

          </div>
        )}

      </div>

    </main>
  );
}