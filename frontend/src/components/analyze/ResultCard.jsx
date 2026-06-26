// import { useState } from "react";

// function ResultCard({ item }) {
//   const [expanded, setExpanded] = useState(false);

//   const clauseType =
//     item.retrieved_label ||
//     item.clause_type ||
//     "Detected Clause";

//   const confidence =
//     item.final_confidence ??
//     item.bert_confidence ??
//     item.legal_bert_confidence ??
//     0;

//   const semanticScore =
//     item.semantic_score ?? "N/A";

//   const bm25Score =
//     item.bm25_score ?? "N/A";

//   const fusionScore =
//     item.fusion_score ?? "N/A";

//   const rerankScore =
//     item.retrieval_rerank_score ?? "N/A";

//   const keywordScore =
//     item.keyword_score ?? "N/A";

//   const clauseText =
//     item.clause_text ||
//     "No clause text available.";

//   const riskLevel =
//     item.risk_level || "Unknown";

//   const reliability =
//     item.reliability_band || "N/A";

//   const explanation =
//     item.explanation ||
//     "No explanation available.";

//   const riskColor =
//     riskLevel === "High"
//       ? "bg-red-100 text-red-700"
//       : riskLevel === "Medium"
//       ? "bg-yellow-100 text-yellow-700"
//       : riskLevel === "Low"
//       ? "bg-green-100 text-green-700"
//       : "bg-gray-100 text-gray-700";

//   return (
//     <div className="bg-white rounded-2xl shadow-md border border-gray-100 p-6">

//       {/* HEADER */}
//       <div className="flex justify-between items-start gap-4 mb-6">
//         <div>
//           <h2 className="text-2xl font-bold mb-2">
//             {clauseType}
//           </h2>

//           <p className="text-gray-500 text-sm">
//             Hybrid Legal Retrieval Result
//           </p>
//         </div>

//         <span
//           className={`px-4 py-2 rounded-full text-sm font-semibold ${riskColor}`}
//         >
//           {riskLevel} Risk
//         </span>
//       </div>

//       {/* METRICS */}
//       <div className="grid md:grid-cols-4 gap-4 mb-6">

//         <MetricCard
//           title="Fusion Score"
//           value={fusionScore}
//         />

//         <MetricCard
//           title="Semantic Score"
//           value={semanticScore}
//         />

//         <MetricCard
//           title="BM25 Score"
//           value={bm25Score}
//         />

//         <MetricCard
//           title="Rerank Score"
//           value={rerankScore}
//         />
//       </div>

//       {/* PREDICTIONS */}
//       <div className="grid md:grid-cols-2 gap-4 mb-6">

//         <InfoCard
//           title="Retrieved Label"
//           value={item.retrieved_label}
//         />

//         <InfoCard
//           title="Classical Prediction"
//           value={item.classical_prediction}
//         />

//         <InfoCard
//           title="Legal-BERT Prediction"
//           value={item.legal_bert_prediction}
//         />

//         <InfoCard
//           title="Reliability"
//           value={reliability}
//         />

//         <InfoCard
//           title="Keyword Score"
//           value={keywordScore}
//         />

//         <InfoCard
//           title="Risk Score"
//           value={item.risk_score}
//         />
//       </div>

//       {/* CONFIDENCE */}
//       <div className="mb-6">
//         <div className="flex justify-between mb-2">

//           <span className="font-semibold">
//             Confidence Score
//           </span>

//           <span className="font-bold text-blue-600">
//             {(confidence * 100).toFixed(1)}%
//           </span>
//         </div>

//         <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">

//           <div
//             className="h-full bg-blue-600 transition-all duration-500"
//             style={{
//               width: `${Math.min(
//                 confidence * 100,
//                 100
//               )}%`,
//             }}
//           />
//         </div>
//       </div>

//       {/* MULTI LABEL */}
//       {item.multi_label_predictions &&
//         item.multi_label_predictions.length > 0 && (

//         <div className="mb-6">

//           <h3 className="font-semibold mb-3">
//             Multi-label Predictions
//           </h3>

//           <div className="flex flex-wrap gap-2">

//             {item.multi_label_predictions.map(
//               (prediction, index) => (

//                 <span
//                   key={index}
//                   className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
//                 >
//                   {prediction.label
//                     || prediction}

//                   {prediction.confidence !== undefined && (
//                     <>
//                       {" "}
//                       -{" "}
//                       {(
//                         prediction.confidence * 100
//                       ).toFixed(1)}
//                       %
//                     </>
//                   )}
//                 </span>
//               )
//             )}
//           </div>
//         </div>
//       )}

//       {/* EXPLANATION */}
//       <div className="bg-indigo-50 rounded-xl p-4 mb-6">

//         <h3 className="font-semibold text-indigo-700 mb-2">
//           AI Explanation
//         </h3>

//         <p className="text-gray-700">
//           {explanation}
//         </p>
//       </div>

//       {/* WARNINGS */}
//       {item.model_disagreement && (

//         <div className="bg-red-100 text-red-700 px-4 py-3 rounded-xl font-semibold mb-4">
//           ⚠ Model disagreement detected between retrieval and Legal-BERT prediction.
//         </div>
//       )}

//       {item.weak_prediction && (

//         <div className="bg-yellow-100 text-yellow-700 px-4 py-3 rounded-xl font-semibold mb-6">
//           ⚠ Weak prediction confidence detected.
//         </div>
//       )}

//       {/* CLAUSE VIEWER */}
//       <div className="bg-gray-50 rounded-xl p-5">

//         <div className="flex justify-between items-center mb-3">

//           <h3 className="font-semibold text-lg">
//             Clause Text
//           </h3>

//           {clauseText.length > 300 && (

//             <button
//               className="text-blue-600 font-semibold"
//               onClick={() =>
//                 setExpanded(!expanded)
//               }
//             >
//               {expanded
//                 ? "Show Less"
//                 : "Read More"}
//             </button>
//           )}
//         </div>

//         <p className="text-gray-700 leading-7 whitespace-pre-line">

//           {expanded
//             ? clauseText
//             : clauseText.slice(0, 300) + "..."}
//         </p>
//       </div>
//     </div>
//   );
// }

// function MetricCard({
//   title,
//   value,
// }) {
//   return (
//     <div className="bg-gray-50 rounded-xl p-4">

//       <p className="text-sm text-gray-500 mb-1">
//         {title}
//       </p>

//       <h3 className="text-xl font-bold text-blue-700">

//         {typeof value === "number"
//           ? value.toFixed(4)
//           : value || "N/A"}
//       </h3>
//     </div>
//   );
// }

// function InfoCard({
//   title,
//   value,
// }) {
//   return (
//     <div className="bg-gray-50 rounded-xl p-4">

//       <p className="text-sm text-gray-500 mb-1">
//         {title}
//       </p>

//       <h3 className="font-semibold">
//         {value || "N/A"}
//       </h3>
//     </div>
//   );
// }

// export default ResultCard;








import { useState } from "react";
import {
  AlertTriangle,
  Brain,
  ChevronDown,
  FileText,
  Gauge,
  Info,
  ShieldAlert,
  Sparkles,
} from "lucide-react";

function ResultCard({ item }) {
  const [expanded, setExpanded] = useState(false);

  const clauseType =
    item.retrieved_label || item.clause_type || "Detected Clause";

  const confidence =
    item.final_confidence ??
    item.bert_confidence ??
    item.legal_bert_confidence ??
    0;

  const semanticScore = item.semantic_score ?? "N/A";
  const bm25Score = item.bm25_score ?? "N/A";
  const fusionScore = item.fusion_score ?? "N/A";
  const rerankScore = item.retrieval_rerank_score ?? "N/A";
  const keywordScore = item.keyword_score ?? "N/A";

  const clauseText =
    item.clause_text || "No clause text available.";

  const riskLevel = item.risk_level || "Unknown";
  const reliability = item.reliability_band || "N/A";
  const explanation = item.explanation || "No explanation available.";

  const riskStyle =
    riskLevel === "High"
      ? "bg-red-100 text-red-700"
      : riskLevel === "Medium"
      ? "bg-amber-100 text-amber-700"
      : riskLevel === "Low"
      ? "bg-emerald-100 text-emerald-700"
      : "bg-slate-100 text-slate-700";

  return (
    <article className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100 transition hover:shadow-xl">
      <div className="mb-7 flex flex-col justify-between gap-5 lg:flex-row lg:items-start">
        <div className="flex items-start gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-100 text-blue-600">
            <Brain size={28} />
          </div>

          <div>
            <h2 className="text-2xl font-bold text-slate-900">
              {clauseType}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Hybrid Legal Retrieval Result
            </p>
          </div>
        </div>

        <span className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-bold ${riskStyle}`}>
          <ShieldAlert size={16} />
          {riskLevel} Risk
        </span>
      </div>

      <div className="mb-7 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard title="Fusion Score" value={fusionScore} />
        <MetricCard title="Semantic Score" value={semanticScore} />
        <MetricCard title="BM25 Score" value={bm25Score} />
        <MetricCard title="Rerank Score" value={rerankScore} />
      </div>

      <div className="mb-7 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <InfoCard title="Retrieved Label" value={item.retrieved_label} />
        <InfoCard title="Classical Prediction" value={item.classical_prediction} />
        <InfoCard title="Legal-BERT Prediction" value={item.legal_bert_prediction} />
        <InfoCard title="Reliability" value={reliability} />
        <InfoCard title="Keyword Score" value={keywordScore} />
        <InfoCard title="Risk Score" value={item.risk_score} />
      </div>

      <div className="mb-7 rounded-2xl bg-slate-50 p-5">
        <div className="mb-3 flex justify-between">
          <span className="flex items-center gap-2 font-bold text-slate-900">
            <Gauge size={18} />
            Confidence Score
          </span>

          <span className="font-bold text-blue-600">
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>

        <div className="h-4 w-full overflow-hidden rounded-full bg-slate-200">
          <div
            className="h-full rounded-full bg-blue-600 transition-all duration-700"
            style={{
              width: `${Math.min(confidence * 100, 100)}%`,
            }}
          />
        </div>
      </div>

      {item.multi_label_predictions &&
        item.multi_label_predictions.length > 0 && (
          <div className="mb-7 rounded-2xl bg-blue-50 p-5">
            <h3 className="mb-3 flex items-center gap-2 font-bold text-blue-700">
              <Sparkles size={18} />
              Multi-label Predictions
            </h3>

            <div className="flex flex-wrap gap-2">
              {item.multi_label_predictions.map((prediction, index) => (
                <span
                  key={index}
                  className="rounded-full bg-white px-3 py-1 text-sm font-semibold text-blue-700"
                >
                  {prediction.label || prediction}

                  {prediction.confidence !== undefined && (
                    <>
                      {" "}
                      - {(prediction.confidence * 100).toFixed(1)}%
                    </>
                  )}
                </span>
              ))}
            </div>
          </div>
        )}

      <div className="mb-7 rounded-2xl bg-indigo-50 p-5">
        <h3 className="mb-2 flex items-center gap-2 font-bold text-indigo-700">
          <Info size={18} />
          AI Explanation
        </h3>

        <p className="leading-7 text-slate-700">
          {explanation}
        </p>
      </div>

      {item.model_disagreement && (
        <div className="mb-4 rounded-2xl bg-red-50 p-4 font-semibold text-red-700">
          <div className="flex items-center gap-2">
            <AlertTriangle size={18} />
            Model disagreement detected between retrieval and Legal-BERT prediction.
          </div>
        </div>
      )}

      {item.weak_prediction && (
        <div className="mb-7 rounded-2xl bg-amber-50 p-4 font-semibold text-amber-700">
          <div className="flex items-center gap-2">
            <AlertTriangle size={18} />
            Weak prediction confidence detected.
          </div>
        </div>
      )}

      <div className="rounded-2xl bg-slate-50 p-5">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900">
            <FileText size={20} />
            Clause Text
          </h3>

          {clauseText.length > 300 && (
            <button
              className="flex items-center gap-1 font-semibold text-blue-600"
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? "Show Less" : "Read More"}
              <ChevronDown
                size={18}
                className={`transition ${
                  expanded ? "rotate-180" : ""
                }`}
              />
            </button>
          )}
        </div>

        <p className="whitespace-pre-line leading-8 text-slate-700">
          {expanded
            ? clauseText
            : clauseText.length > 300
            ? `${clauseText.slice(0, 300)}...`
            : clauseText}
        </p>
      </div>
    </article>
  );
}

function MetricCard({ title, value }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-5">
      <p className="text-sm font-semibold text-slate-500">
        {title}
      </p>

      <h3 className="mt-2 text-2xl font-bold text-blue-700">
        {typeof value === "number"
          ? value.toFixed(4)
          : value || "N/A"}
      </h3>
    </div>
  );
}

function InfoCard({ title, value }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-5">
      <p className="text-sm font-semibold text-slate-500">
        {title}
      </p>

      <h3 className="mt-2 font-bold text-slate-900">
        {value || "N/A"}
      </h3>
    </div>
  );
}

export default ResultCard;