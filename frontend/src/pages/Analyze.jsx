import { useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";
import ResultCard from "../components/analyze/ResultCard";

function Analyze() {
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const res = await axios.post(
        "http://localhost:8000/analyze",
        {
          query: input,
        }
      );

      setResults(res.data || []);
      setSummary(null);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to backend analysis service."
      );
    }

    setLoading(false);
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* HEADER */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-3">
            AI Contract Intelligence Dashboard
          </h1>

          <p className="text-gray-600 text-lg">
            Hybrid Legal Retrieval + Risk Analysis
          </p>
        </div>

        {/* INPUT */}
        <div className="bg-white rounded-2xl shadow-md p-5 mb-8">
          <div className="flex gap-3 items-end">
            <textarea
              placeholder="Analyze a clause (e.g. termination clause, liability clause, renewal clause)"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              rows={1}
              className="flex-1 border border-gray-300 px-4 py-3 rounded-xl resize-none outline-none focus:ring-2 focus:ring-blue-500 min-h-[56px] max-h-32 overflow-y-auto"
              onInput={(e) => {
                e.target.style.height = "auto";
                e.target.style.height = `${Math.min(
                  e.target.scrollHeight,
                  140
                )}px`;
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleAnalyze();
                }
              }}
            />

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-xl font-semibold transition-all"
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>
        </div>

        {/* ERROR */}
        {error && (
          <div className="bg-red-100 text-red-700 px-5 py-4 rounded-xl mb-6 font-medium">
            {error}
          </div>
        )}

        {/* SUMMARY DASHBOARD */}
        {summary && (
          <div className="grid md:grid-cols-4 gap-5 mb-10">
            <div className="bg-white rounded-2xl shadow-md p-5">
              <p className="text-gray-500 mb-2 text-sm">
                Overall Risk
              </p>

              <h2 className="text-2xl font-bold text-red-600">
                {summary.overall_risk}
              </h2>
            </div>

            <div className="bg-white rounded-2xl shadow-md p-5">
              <p className="text-gray-500 mb-2 text-sm">
                Average Confidence
              </p>

              <h2 className="text-2xl font-bold text-blue-600">
                {(
                  (summary.average_confidence || 0) * 100
                ).toFixed(1)}%
              </h2>
            </div>

            <div className="bg-white rounded-2xl shadow-md p-5">
              <p className="text-gray-500 mb-2 text-sm">
                High Confidence Clauses
              </p>

              <h2 className="text-2xl font-bold text-green-600">
                {summary.high_confidence_clauses}
              </h2>
            </div>

            <div className="bg-white rounded-2xl shadow-md p-5">
              <p className="text-gray-500 mb-2 text-sm">
                Top Labels
              </p>

              <div className="flex flex-wrap gap-2 mt-2">
                {(summary.top_detected_labels || []).map(
                  (label, index) => (
                    <span
                      key={index}
                      className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
                    >
                      {label}
                    </span>
                  )
                )}
              </div>
            </div>
          </div>
        )}

        {/* LOADING */}
        {loading && (
          <div className="text-blue-600 font-semibold text-lg">
            Running Hybrid Retrieval Pipeline...
          </div>
        )}

        {/* EMPTY */}
        {!loading && results.length === 0 && (
          <div className="bg-white rounded-2xl shadow-md p-10 text-center text-gray-500">
            No analysis results yet.
          </div>
        )}

        {/* RESULTS */}
        <div className="space-y-6">
          {results.map((item, index) => (
            <ResultCard
              key={index}
              item={item}
            />
          ))}
        </div>
      </div>
    </Layout>
  );
}

export default Analyze;
