import { useState } from "react";

function ResultCard({ item }) {
  const [expanded, setExpanded] = useState(false);

  const clauseType =
    item.retrieved_label ||
    item.clause_type ||
    "Detected Clause";

  const confidence =
    item.final_confidence ??
    item.bert_confidence ??
    item.legal_bert_confidence ??
    0;

  const semanticScore =
    item.semantic_score ?? "N/A";

  const bm25Score =
    item.bm25_score ?? "N/A";

  const fusionScore =
    item.fusion_score ?? "N/A";

  const rerankScore =
    item.retrieval_rerank_score ?? "N/A";

  const keywordScore =
    item.keyword_score ?? "N/A";

  const clauseText =
    item.clause_text ||
    "No clause text available.";

  const riskLevel =
    item.risk_level || "Unknown";

  const reliability =
    item.reliability_band || "N/A";

  const explanation =
    item.explanation ||
    "No explanation available.";

  const riskColor =
    riskLevel === "High"
      ? "bg-red-100 text-red-700"
      : riskLevel === "Medium"
      ? "bg-yellow-100 text-yellow-700"
      : riskLevel === "Low"
      ? "bg-green-100 text-green-700"
      : "bg-gray-100 text-gray-700";

  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-100 p-6">

      {/* HEADER */}
      <div className="flex justify-between items-start gap-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold mb-2">
            {clauseType}
          </h2>

          <p className="text-gray-500 text-sm">
            Hybrid Legal Retrieval Result
          </p>
        </div>

        <span
          className={`px-4 py-2 rounded-full text-sm font-semibold ${riskColor}`}
        >
          {riskLevel} Risk
        </span>
      </div>

      {/* METRICS */}
      <div className="grid md:grid-cols-4 gap-4 mb-6">

        <MetricCard
          title="Fusion Score"
          value={fusionScore}
        />

        <MetricCard
          title="Semantic Score"
          value={semanticScore}
        />

        <MetricCard
          title="BM25 Score"
          value={bm25Score}
        />

        <MetricCard
          title="Rerank Score"
          value={rerankScore}
        />
      </div>

      {/* PREDICTIONS */}
      <div className="grid md:grid-cols-2 gap-4 mb-6">

        <InfoCard
          title="Retrieved Label"
          value={item.retrieved_label}
        />

        <InfoCard
          title="Classical Prediction"
          value={item.classical_prediction}
        />

        <InfoCard
          title="Legal-BERT Prediction"
          value={item.legal_bert_prediction}
        />

        <InfoCard
          title="Reliability"
          value={reliability}
        />

        <InfoCard
          title="Keyword Score"
          value={keywordScore}
        />

        <InfoCard
          title="Risk Score"
          value={item.risk_score}
        />
      </div>

      {/* CONFIDENCE */}
      <div className="mb-6">
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
            className="h-full bg-blue-600 transition-all duration-500"
            style={{
              width: `${Math.min(
                confidence * 100,
                100
              )}%`,
            }}
          />
        </div>
      </div>

      {/* MULTI LABEL */}
      {item.multi_label_predictions &&
        item.multi_label_predictions.length > 0 && (

        <div className="mb-6">

          <h3 className="font-semibold mb-3">
            Multi-label Predictions
          </h3>

          <div className="flex flex-wrap gap-2">

            {item.multi_label_predictions.map(
              (prediction, index) => (

                <span
                  key={index}
                  className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
                >
                  {prediction.label
                    || prediction}

                  {prediction.confidence !== undefined && (
                    <>
                      {" "}
                      -{" "}
                      {(
                        prediction.confidence * 100
                      ).toFixed(1)}
                      %
                    </>
                  )}
                </span>
              )
            )}
          </div>
        </div>
      )}

      {/* EXPLANATION */}
      <div className="bg-indigo-50 rounded-xl p-4 mb-6">

        <h3 className="font-semibold text-indigo-700 mb-2">
          AI Explanation
        </h3>

        <p className="text-gray-700">
          {explanation}
        </p>
      </div>

      {/* WARNINGS */}
      {item.model_disagreement && (

        <div className="bg-red-100 text-red-700 px-4 py-3 rounded-xl font-semibold mb-4">
          ⚠ Model disagreement detected between retrieval and Legal-BERT prediction.
        </div>
      )}

      {item.weak_prediction && (

        <div className="bg-yellow-100 text-yellow-700 px-4 py-3 rounded-xl font-semibold mb-6">
          ⚠ Weak prediction confidence detected.
        </div>
      )}

      {/* CLAUSE VIEWER */}
      <div className="bg-gray-50 rounded-xl p-5">

        <div className="flex justify-between items-center mb-3">

          <h3 className="font-semibold text-lg">
            Clause Text
          </h3>

          {clauseText.length > 300 && (

            <button
              className="text-blue-600 font-semibold"
              onClick={() =>
                setExpanded(!expanded)
              }
            >
              {expanded
                ? "Show Less"
                : "Read More"}
            </button>
          )}
        </div>

        <p className="text-gray-700 leading-7 whitespace-pre-line">

          {expanded
            ? clauseText
            : clauseText.slice(0, 300) + "..."}
        </p>
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
}) {
  return (
    <div className="bg-gray-50 rounded-xl p-4">

      <p className="text-sm text-gray-500 mb-1">
        {title}
      </p>

      <h3 className="text-xl font-bold text-blue-700">

        {typeof value === "number"
          ? value.toFixed(4)
          : value || "N/A"}
      </h3>
    </div>
  );
}

function InfoCard({
  title,
  value,
}) {
  return (
    <div className="bg-gray-50 rounded-xl p-4">

      <p className="text-sm text-gray-500 mb-1">
        {title}
      </p>

      <h3 className="font-semibold">
        {value || "N/A"}
      </h3>
    </div>
  );
}

export default ResultCard;