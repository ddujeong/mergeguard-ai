"use client";

import { useState } from "react";

import { analyzePrApi } from "@/api/reviewApi";

import ReactMarkdown from "react-markdown";

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

            <div className="rounded-lg border bg-white p-5 text-black">

              <h2 className="mb-3 text-xl font-bold">
                위험도 분석
              </h2>

              <p
                className={
                  result.risk_analysis.risk_level === "HIGH"
                    ? "text-red-600 font-bold"
                    : result.risk_analysis.risk_level === "MEDIUM"
                      ? "text-yellow-600 font-bold"
                      : "text-green-600 font-bold"
                }
              >
                위험도: {result.risk_analysis.risk_level}
              </p>

              <p>
                점수:
                {" "}
                {result.risk_analysis.risk_score}
              </p>

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