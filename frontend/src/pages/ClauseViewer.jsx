// import Layout from "../components/layout/Layout";

// const sampleClauses = [
//   {
//     clause_type: "Termination",
//     risk_level: "HIGH",
//     page_number: 3,
//     text: "This contract may be terminated without notice."
//   },
//   {
//     clause_type: "Payment Terms",
//     risk_level: "MEDIUM",
//     page_number: 2,
//     text: "Payment must be made within 30 days of invoice."
//   },
//   {
//     clause_type: "Confidentiality",
//     risk_level: "LOW",
//     page_number: 1,
//     text: "All parties must maintain confidentiality."
//   }
// ];

// function ClauseViewer() {
//   return (
//     <Layout>
//       <h2 className="text-3xl font-bold mb-8 text-center">Clause Viewer</h2>

//       <div className="max-w-4xl mx-auto space-y-6">
//         {sampleClauses.map((clause, index) => (
//           <div
//             key={index}
//             className={`p-5 rounded-lg shadow-md ${
//               clause.risk_level === "HIGH"
//                 ? "bg-red-100 border-l-4 border-red-500"
//                 : clause.risk_level === "MEDIUM"
//                 ? "bg-yellow-100 border-l-4 border-yellow-500"
//                 : "bg-green-100 border-l-4 border-green-500"
//             }`}
//           >
//             <div className="flex justify-between mb-2">
//               <span className="font-semibold">{clause.clause_type}</span>
//               <span className="text-sm">
//                 Risk: {clause.risk_level}
//               </span>
//             </div>

//             <p className="text-gray-700">{clause.text}</p>

//             <p className="text-xs text-gray-500 mt-2">
//               Page: {clause.page_number}
//             </p>
//           </div>
//         ))}
//       </div>
//     </Layout>
//   );
// }

// export default ClauseViewer;


// week 3 thursdayyyyyyy
// import Layout from "../components/layout/Layout";
// import { useEffect, useState } from "react";
// import { getContracts } from "../services/api";

// function ClauseViewer() {
//   const [contracts, setContracts] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");

//   useEffect(() => {
//     fetchContracts();
//   }, []);

//   const fetchContracts = async () => {
//     try {
//       setLoading(true);

//       const data = await getContracts();

//       console.log("Contracts response:", data);

//       setContracts(data || []);
//     } catch (err) {
//       console.log("Contracts error:", err);

//       setError("Failed to load contracts.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Layout>
//       <h2 className="text-3xl font-bold mb-8 text-center">
//         Clause Viewer
//       </h2>

//       {/* LOADING */}
//       {loading && (
//         <div className="text-center text-gray-600">
//           Loading contracts...
//         </div>
//       )}

//       {/* ERROR */}
//       {error && (
//         <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6 max-w-3xl mx-auto">
//           {error}
//         </div>
//       )}

//       {/* EMPTY */}
//       {!loading && contracts.length === 0 && !error && (
//         <div className="bg-white p-6 rounded shadow text-center max-w-3xl mx-auto">
//           No contracts found.
//         </div>
//       )}

//       {/* CONTRACTS */}
//       <div className="max-w-4xl mx-auto space-y-6">
//         {contracts.map((contract, index) => (
//           <div
//             key={index}
//             className={`p-5 rounded-lg shadow-md ${
//               contract.risk_level === "HIGH"
//                 ? "bg-red-100 border-l-4 border-red-500"
//                 : contract.risk_level === "MEDIUM"
//                 ? "bg-yellow-100 border-l-4 border-yellow-500"
//                 : "bg-green-100 border-l-4 border-green-500"
//             }`}
//           >
//             <div className="flex justify-between mb-2">
//               <span className="font-semibold">
//                 {contract.clause_type || "Unknown Clause"}
//               </span>

//               <span className="text-sm">
//                 Risk: {contract.risk_level || "N/A"}
//               </span>
//             </div>

//             <p className="text-gray-700">
//               {contract.text || contract.clause_text || "No clause text available."}
//             </p>

//             <p className="text-xs text-gray-500 mt-2">
//               Page: {contract.page_number || "N/A"}
//             </p>
//           </div>
//         ))}
//       </div>
//     </Layout>
//   );
// }

// export default ClauseViewer;


// week 4 thursdayyyyyyyyyyyyyyyyyyyyy
import Layout from "../components/layout/Layout";
import { useEffect, useState } from "react";
import { getContracts } from "../services/api";

function ClauseViewer() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchContracts();
  }, []);

  const fetchContracts = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getContracts();

      console.log("Contracts response:", data);

      setContracts(data || []);
    } catch (err) {
      console.log("Contracts error:", err);
      setError("Failed to load contracts.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h2 className="text-3xl font-bold mb-8 text-center">
        Uploaded Contracts
      </h2>

      {loading && (
        <div className="text-center text-gray-600">
          Loading contracts...
        </div>
      )}

      {error && (
        <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6 max-w-3xl mx-auto">
          {error}
        </div>
      )}

      {!loading && contracts.length === 0 && !error && (
        <div className="bg-white p-6 rounded shadow text-center max-w-3xl mx-auto">
          No contracts found.
        </div>
      )}

      <div className="max-w-4xl mx-auto space-y-6">
        {contracts.map((contract, index) => (
          <div
            key={index}
            className="bg-white p-5 rounded-lg shadow-md border-l-4 border-blue-500"
          >
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-xl font-bold">
                {contract.filename || "Untitled Contract"}
              </h3>

              <span
                className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  contract.status === "uploaded"
                    ? "bg-green-100 text-green-700"
                    : contract.status === "failed"
                    ? "bg-red-100 text-red-700"
                    : "bg-yellow-100 text-yellow-700"
                }`}
              >
                {contract.status || "Unknown"}
              </span>
            </div>

            <div className="space-y-2 text-gray-700">
              <p>
                <strong>Contract ID:</strong>{" "}
                {contract.contract_id || "N/A"}
              </p>

              <p>
                <strong>Upload Time:</strong>{" "}
                {contract.upload_time
                  ? new Date(contract.upload_time).toLocaleString()
                  : "N/A"}
              </p>

              <p>
                <strong>Error Message:</strong>{" "}
                {contract.error_message || "None"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}

export default ClauseViewer;