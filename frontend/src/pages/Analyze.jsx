// import { useState } from "react";
// import axios from "axios";
// import Layout from "../components/layout/Layout";
// import ResultCard from "../components/analyze/ResultCard";

// function Analyze() {
//   const [input, setInput] = useState("");
//   const [results, setResults] = useState([]);
//   const [summary, setSummary] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const handleAnalyze = async () => {
//     if (!input.trim()) return;

//     setLoading(true);
//     setError("");
//     setResults([]);

//     try {
//       const res = await axios.post(
//         "http://localhost:8000/analyze",
//         {
//           query: input,
//         }
//       );

//       setResults(res.data || []);
//       setSummary(null);
//     } catch (err) {
//       console.error(err);

//       setError(
//         "Unable to connect to backend analysis service."
//       );
//     }

//     setLoading(false);
//   };

//   return (
//     <Layout>
//       <div className="max-w-7xl mx-auto px-4 py-8">
//         {/* HEADER */}
//         <div className="mb-8">
//           <h1 className="text-4xl font-bold mb-3">
//             AI Contract Intelligence Dashboard
//           </h1>

//           <p className="text-gray-600 text-lg">
//             Hybrid Legal Retrieval + Risk Analysis
//           </p>
//         </div>

//         {/* INPUT */}
//         <div className="bg-white rounded-2xl shadow-md p-5 mb-8">
//           <div className="flex gap-3 items-end">
//             <textarea
//               placeholder="Analyze a clause (e.g. termination clause, liability clause, renewal clause)"
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               rows={1}
//               className="flex-1 border border-gray-300 px-4 py-3 rounded-xl resize-none outline-none focus:ring-2 focus:ring-blue-500 min-h-[56px] max-h-32 overflow-y-auto"
//               onInput={(e) => {
//                 e.target.style.height = "auto";
//                 e.target.style.height = `${Math.min(
//                   e.target.scrollHeight,
//                   140
//                 )}px`;
//               }}
//               onKeyDown={(e) => {
//                 if (e.key === "Enter" && !e.shiftKey) {
//                   e.preventDefault();
//                   handleAnalyze();
//                 }
//               }}
//             />

//             <button
//               onClick={handleAnalyze}
//               disabled={loading}
//               className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-xl font-semibold transition-all"
//             >
//               {loading ? "Analyzing..." : "Analyze"}
//             </button>
//           </div>
//         </div>

//         {/* ERROR */}
//         {error && (
//           <div className="bg-red-100 text-red-700 px-5 py-4 rounded-xl mb-6 font-medium">
//             {error}
//           </div>
//         )}

//         {/* SUMMARY DASHBOARD */}
//         {summary && (
//           <div className="grid md:grid-cols-4 gap-5 mb-10">
//             <div className="bg-white rounded-2xl shadow-md p-5">
//               <p className="text-gray-500 mb-2 text-sm">
//                 Overall Risk
//               </p>

//               <h2 className="text-2xl font-bold text-red-600">
//                 {summary.overall_risk}
//               </h2>
//             </div>

//             <div className="bg-white rounded-2xl shadow-md p-5">
//               <p className="text-gray-500 mb-2 text-sm">
//                 Average Confidence
//               </p>

//               <h2 className="text-2xl font-bold text-blue-600">
//                 {(
//                   (summary.average_confidence || 0) * 100
//                 ).toFixed(1)}%
//               </h2>
//             </div>

//             <div className="bg-white rounded-2xl shadow-md p-5">
//               <p className="text-gray-500 mb-2 text-sm">
//                 High Confidence Clauses
//               </p>

//               <h2 className="text-2xl font-bold text-green-600">
//                 {summary.high_confidence_clauses}
//               </h2>
//             </div>

//             <div className="bg-white rounded-2xl shadow-md p-5">
//               <p className="text-gray-500 mb-2 text-sm">
//                 Top Labels
//               </p>

//               <div className="flex flex-wrap gap-2 mt-2">
//                 {(summary.top_detected_labels || []).map(
//                   (label, index) => (
//                     <span
//                       key={index}
//                       className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
//                     >
//                       {label}
//                     </span>
//                   )
//                 )}
//               </div>
//             </div>
//           </div>
//         )}

//         {/* LOADING */}
//         {loading && (
//           <div className="text-blue-600 font-semibold text-lg">
//             Running Hybrid Retrieval Pipeline...
//           </div>
//         )}

//         {/* EMPTY */}
//         {!loading && results.length === 0 && (
//           <div className="bg-white rounded-2xl shadow-md p-10 text-center text-gray-500">
//             No analysis results yet.
//           </div>
//         )}

//         {/* RESULTS */}
//         <div className="space-y-6">
//           {results.map((item, index) => (
//             <ResultCard
//               key={index}
//               item={item}
//             />
//           ))}
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Analyze;














import { useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";
import ResultCard from "../components/analyze/ResultCard";
import {
  Brain,
  Search,
  Sparkles,
  AlertCircle,
  Loader2,
  FileSearch,
  ShieldAlert,
  Gauge,
  Tags,
} from "lucide-react";

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
      setError("Unable to connect to backend analysis service.");
    }

    setLoading(false);
  };

  return (
    <Layout>
      <div className="space-y-8">
        <section className="rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-10 text-white shadow-xl">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-white/10 px-5 py-2 text-sm">
            <Brain size={16} />
            AI Legal Risk Analysis
          </div>

          <h1 className="text-5xl font-bold mb-4">
            Analyze Contract
          </h1>

          <p className="max-w-3xl text-lg text-slate-300">
            Run hybrid legal retrieval, Legal-BERT prediction, risk scoring,
            confidence analysis, and explainable AI insights for contract clauses.
          </p>
        </section>

        <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
          <div className="mb-6 flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-100 text-blue-600">
              <FileSearch size={28} />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900">
                Clause Analysis Query
              </h2>
              <p className="text-sm text-slate-500">
                Enter a clause type or legal query to analyze using the backend pipeline.
              </p>
            </div>
          </div>

          <div className="flex flex-col gap-4 lg:flex-row lg:items-end">
            <div className="relative flex-1">
              <Search
                size={20}
                className="absolute left-4 top-4 text-slate-400"
              />

              <textarea
                placeholder="Analyze a clause, e.g. termination clause, liability clause, renewal clause..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={1}
                className="min-h-[58px] max-h-36 w-full resize-none rounded-2xl border border-slate-200 bg-slate-50 py-4 pl-12 pr-4 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="flex items-center justify-center gap-2 rounded-2xl bg-blue-600 px-8 py-4 font-semibold text-white shadow-lg transition hover:bg-blue-700 disabled:bg-slate-400"
            >
              {loading ? (
                <>
                  <Loader2 size={20} className="animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  Analyze
                </>
              )}
            </button>
          </div>

          <div className="mt-5 flex flex-wrap gap-3">
            {[
              "termination clause",
              "confidentiality clause",
              "payment obligations",
              "renewal term",
            ].map((item) => (
              <button
                key={item}
                onClick={() => setInput(item)}
                className="rounded-full bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-600 transition hover:bg-blue-100"
              >
                {item}
              </button>
            ))}
          </div>
        </section>

        {error && (
          <section className="rounded-3xl border border-red-100 bg-red-50 p-6 text-red-700">
            <div className="flex items-center gap-3">
              <AlertCircle />
              <div>
                <h3 className="font-bold">Analysis Failed</h3>
                <p>{error}</p>
              </div>
            </div>
          </section>
        )}

        {summary && (
          <section className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
            <SummaryCard
              title="Overall Risk"
              value={summary.overall_risk}
              icon={ShieldAlert}
              color="bg-red-100 text-red-600"
            />

            <SummaryCard
              title="Average Confidence"
              value={`${((summary.average_confidence || 0) * 100).toFixed(
                1
              )}%`}
              icon={Gauge}
              color="bg-blue-100 text-blue-600"
            />

            <SummaryCard
              title="High Confidence Clauses"
              value={summary.high_confidence_clauses}
              icon={Sparkles}
              color="bg-emerald-100 text-emerald-600"
            />

            <SummaryCard
              title="Top Labels"
              value={(summary.top_detected_labels || []).join(", ") || "N/A"}
              icon={Tags}
              color="bg-purple-100 text-purple-600"
            />
          </section>
        )}

        {loading && (
          <section className="rounded-3xl bg-white p-10 text-center shadow-sm border border-slate-100">
            <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-blue-50">
              <Loader2 className="animate-spin text-blue-600" size={38} />
            </div>

            <h3 className="text-2xl font-bold text-slate-900">
              Running Hybrid Retrieval Pipeline...
            </h3>

            <p className="mt-2 text-slate-500">
              Retrieving clauses, scoring risk, comparing predictions, and generating explanations.
            </p>
          </section>
        )}

        {!loading && results.length === 0 && !error && (
          <section className="rounded-3xl bg-white p-12 text-center shadow-sm border border-slate-100">
            <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-blue-50 text-blue-600">
              <Brain size={38} />
            </div>

            <h3 className="text-2xl font-bold text-slate-900">
              No analysis results yet
            </h3>

            <p className="mt-2 text-slate-500">
              Enter a legal query above and run AI-powered contract analysis.
            </p>
          </section>
        )}

        <div className="space-y-6">
          {results.map((item, index) => (
            <ResultCard key={index} item={item} />
          ))}
        </div>
      </div>
    </Layout>
  );
}

function SummaryCard({ title, value, icon: Icon, color }) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm border border-slate-100">
      <div className={`mb-5 flex h-12 w-12 items-center justify-center rounded-2xl ${color}`}>
        <Icon size={24} />
      </div>

      <p className="text-sm font-semibold text-slate-500">
        {title}
      </p>

      <h3 className="mt-2 text-2xl font-bold text-slate-900">
        {value || "N/A"}
      </h3>
    </div>
  );
}

export default Analyze;