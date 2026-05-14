import Layout from "../components/layout/Layout";

const sampleClauses = [
  {
    clause_type: "Termination",
    risk_level: "HIGH",
    page_number: 3,
    text: "This contract may be terminated without notice."
  },
  {
    clause_type: "Payment Terms",
    risk_level: "MEDIUM",
    page_number: 2,
    text: "Payment must be made within 30 days of invoice."
  },
  {
    clause_type: "Confidentiality",
    risk_level: "LOW",
    page_number: 1,
    text: "All parties must maintain confidentiality."
  }
];

function ClauseViewer() {
  return (
    <Layout>
      <h2 className="text-3xl font-bold mb-8 text-center">Clause Viewer</h2>

      <div className="max-w-4xl mx-auto space-y-6">
        {sampleClauses.map((clause, index) => (
          <div
            key={index}
            className={`p-5 rounded-lg shadow-md ${
              clause.risk_level === "HIGH"
                ? "bg-red-100 border-l-4 border-red-500"
                : clause.risk_level === "MEDIUM"
                ? "bg-yellow-100 border-l-4 border-yellow-500"
                : "bg-green-100 border-l-4 border-green-500"
            }`}
          >
            <div className="flex justify-between mb-2">
              <span className="font-semibold">{clause.clause_type}</span>
              <span className="text-sm">
                Risk: {clause.risk_level}
              </span>
            </div>

            <p className="text-gray-700">{clause.text}</p>

            <p className="text-xs text-gray-500 mt-2">
              Page: {clause.page_number}
            </p>
          </div>
        ))}
      </div>
    </Layout>
  );
}

export default ClauseViewer;