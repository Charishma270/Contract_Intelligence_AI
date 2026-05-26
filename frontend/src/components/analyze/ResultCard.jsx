// import { useState } from "react";

// function ResultCard({ item }) {
//   const [expanded, setExpanded] = useState(false);

//   return (
//     <div className="bg-white rounded-xl shadow-md p-6">
      
//       {/* TOP */}
//       <div className="flex justify-between items-center mb-4">
//         <h2 className="text-2xl font-bold">
//           {item.clause_type}
//         </h2>

//         <span
//           className={`px-4 py-2 rounded-full text-sm font-semibold ${
//             item.risk_level === "High"
//               ? "bg-red-100 text-red-600"
//               : item.risk_level === "Medium"
//               ? "bg-yellow-100 text-yellow-700"
//               : "bg-green-100 text-green-700"
//           }`}
//         >
//           {item.risk_level} Risk
//         </span>
//       </div>

//       {/* DETAILS */}
//       <div className="grid md:grid-cols-2 gap-3 mb-5">
//         <p>
//           <strong>Retrieved Label:</strong>{" "}
//           {item.retrieved_label}
//         </p>

//         <p>
//           <strong>Transformer Prediction:</strong>{" "}
//           {item.legal_bert_prediction}
//         </p>

//         <p>
//           <strong>Similarity Score:</strong>{" "}
//           {item.similarity_score}
//         </p>

//         <p>
//           <strong>Hybrid Score:</strong>{" "}
//           {item.hybrid_score}
//         </p>
//       </div>

//       {/* CONFIDENCE */}
//       <div className="mb-5">
//         <div className="flex justify-between mb-2">
//           <span className="font-semibold">
//             Confidence Score
//           </span>

//           <span className="font-bold text-blue-600">
//             {(item.legal_bert_confidence * 100).toFixed(1)}%
//           </span>
//         </div>

//         <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
//           <div
//             className="h-full bg-blue-600"
//             style={{
//               width: `${
//                 item.legal_bert_confidence * 100
//               }%`,
//             }}
//           />
//         </div>
//       </div>

//       {/* WARNING */}
//       {item.model_disagreement && (
//         <div className="bg-red-100 text-red-700 px-4 py-3 rounded-lg font-semibold mb-5">
//           ⚠ Model Disagreement Detected
//         </div>
//       )}

//       {/* CLAUSE VIEWER */}
//       <div className="bg-gray-100 rounded-lg p-4">
//         <h3 className="font-bold mb-3">
//           Clause Text
//         </h3>

//         <p className="text-gray-700">
//           {expanded
//             ? item.clause_text
//             : item.clause_text.slice(0, 100) + "..."}
//         </p>

//         <button
//           className="text-blue-600 mt-3 font-semibold"
//           onClick={() => setExpanded(!expanded)}
//         >
//           {expanded ? "Show Less" : "Read More"}
//         </button>
//       </div>
//     </div>
//   );
// }

// export default ResultCard;



//tuesdayyyyyyy(week 3)
import { useState } from "react";

function ResultCard({ item }) {
  const [expanded, setExpanded] = useState(false);

  const clauseType =
    item.retrieved_label || item.clause_type || "Detected Clause";

  const confidence =
    item.bert_confidence ??
    item.final_confidence ??
    item.legal_bert_confidence ??
    0;

  const semanticScore =
    item.semantic_score ?? item.similarity_score ?? "N/A";

  const finalScore =
    item.final_confidence ??
    item.hybrid_score ??
    item.retrieval_rerank_score ??
    "N/A";

  const clauseText = item.clause_text || "No clause text available.";

  const riskLevel = item.risk_level || "Unknown";

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      {/* TOP */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">
          {clauseType}
        </h2>

        <span
          className={`px-4 py-2 rounded-full text-sm font-semibold ${
            riskLevel === "High"
              ? "bg-red-100 text-red-600"
              : riskLevel === "Medium"
              ? "bg-yellow-100 text-yellow-700"
              : riskLevel === "Low"
              ? "bg-green-100 text-green-700"
              : "bg-gray-100 text-gray-700"
          }`}
        >
          {riskLevel} Risk
        </span>
      </div>

      {/* DETAILS */}
      <div className="grid md:grid-cols-2 gap-3 mb-5">
        <p>
          <strong>Retrieved Label:</strong>{" "}
          {item.retrieved_label || "N/A"}
        </p>

        <p>
          <strong>Classical Prediction:</strong>{" "}
          {item.classical_prediction || "N/A"}
        </p>

        <p>
          <strong>Legal-BERT Prediction:</strong>{" "}
          {item.legal_bert_prediction || "N/A"}
        </p>

        <p>
          <strong>Semantic Score:</strong>{" "}
          {semanticScore}
        </p>

        <p>
          <strong>Keyword Score:</strong>{" "}
          {item.keyword_score ?? "N/A"}
        </p>

        <p>
          <strong>Final Confidence:</strong>{" "}
          {finalScore}
        </p>

        <p>
          <strong>Retrieval Rerank Score:</strong>{" "}
          {item.retrieval_rerank_score ?? "N/A"}
        </p>

        <p>
          <strong>Reliability:</strong>{" "}
          {item.reliability_band || "N/A"}
        </p>

        <p>
          <strong>Risk Score:</strong>{" "}
          {item.risk_score ?? "N/A"}
        </p>

        <p>
          <strong>Weak Prediction:</strong>{" "}
          {item.weak_prediction ? "Yes" : "No"}
        </p>
      </div>

      {/* CONFIDENCE */}
      <div className="mb-5">
        <div className="flex justify-between mb-2">
          <span className="font-semibold">
            Confidence Score
          </span>

          <span className="font-bold text-blue-600">
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>

        <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-blue-600"
            style={{
              width: `${Math.min(confidence * 100, 100)}%`,
            }}
          />
        </div>
      </div>

      {/* MULTI LABEL PREDICTIONS */}
      {item.multi_label_predictions &&
        item.multi_label_predictions.length > 0 && (
          <div className="mb-5">
            <h3 className="font-bold mb-2">
              Multi-Label Predictions
            </h3>

            <div className="flex flex-wrap gap-2">
              {item.multi_label_predictions.map((prediction, index) => (
                <span
                  key={index}
                  className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
                >
                  {prediction.label} -{" "}
                  {((prediction.confidence ?? 0) * 100).toFixed(1)}%
                </span>
              ))}
            </div>
          </div>
        )}

      {/* EXPLANATION */}
      {item.explanation && (
        <div className="bg-blue-50 text-blue-700 px-4 py-3 rounded-lg font-medium mb-5">
          <strong>Explanation:</strong> {item.explanation}
        </div>
      )}

      {/* WARNING */}
      {item.model_disagreement && (
        <div className="bg-red-100 text-red-700 px-4 py-3 rounded-lg font-semibold mb-5">
          ⚠ Model Disagreement Detected
        </div>
      )}

      {/* CLAUSE VIEWER */}
      <div className="bg-gray-100 rounded-lg p-4">
        <h3 className="font-bold mb-3">
          Clause Text
        </h3>

        <p className="text-gray-700">
          {expanded
            ? clauseText
            : clauseText.slice(0, 150) + "..."}
        </p>

        {clauseText.length > 150 && (
          <button
            className="text-blue-600 mt-3 font-semibold"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? "Show Less" : "Read More"}
          </button>
        )}
      </div>
    </div>
  );
}

export default ResultCard;