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
//       setError("");

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
//         Uploaded Contracts
//       </h2>

//       {loading && (
//         <div className="text-center text-gray-600">
//           Loading contracts...
//         </div>
//       )}

//       {error && (
//         <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6 max-w-3xl mx-auto">
//           {error}
//         </div>
//       )}

//       {!loading && contracts.length === 0 && !error && (
//         <div className="bg-white p-6 rounded shadow text-center max-w-3xl mx-auto">
//           No contracts found.
//         </div>
//       )}

//       <div className="max-w-4xl mx-auto space-y-6">
//         {contracts.map((contract, index) => (
//           <div
//             key={index}
//             className="bg-white p-5 rounded-lg shadow-md border-l-4 border-blue-500"
//           >
//             <div className="flex justify-between items-center mb-3">
//               <h3 className="text-xl font-bold">
//                 {contract.filename || "Untitled Contract"}
//               </h3>

//               <span
//                 className={`px-3 py-1 rounded-full text-sm font-semibold ${
//                   contract.status === "uploaded"
//                     ? "bg-green-100 text-green-700"
//                     : contract.status === "failed"
//                     ? "bg-red-100 text-red-700"
//                     : "bg-yellow-100 text-yellow-700"
//                 }`}
//               >
//                 {contract.status || "Unknown"}
//               </span>
//             </div>

//             <div className="space-y-2 text-gray-700">
//               <p>
//                 <strong>Contract ID:</strong>{" "}
//                 {contract.contract_id || "N/A"}
//               </p>

//               <p>
//                 <strong>Upload Time:</strong>{" "}
//                 {contract.upload_time
//                   ? new Date(contract.upload_time).toLocaleString()
//                   : "N/A"}
//               </p>

//               <p>
//                 <strong>Error Message:</strong>{" "}
//                 {contract.error_message || "None"}
//               </p>
//             </div>
//           </div>
//         ))}
//       </div>
//     </Layout>
//   );
// }

// export default ClauseViewer;






// changes 


import { useNavigate } from "react-router-dom";
import Layout from "../components/layout/Layout";
import { useEffect, useState } from "react";
import { getContracts } from "../services/api";
import {
  FileText,
  Search,
  RefreshCw,
  Calendar,
  Hash,
  AlertCircle,
  CheckCircle,
  Clock,
  Eye,
} from "lucide-react";

function ClauseViewer() {
  const [contracts, setContracts] = useState([]);
  const [filteredContracts, setFilteredContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const navigate = useNavigate();

  useEffect(() => {
    fetchContracts();
  }, []);

  useEffect(() => {
    filterContracts();
  }, [contracts, searchTerm, statusFilter]);

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

  const filterContracts = () => {
    let updatedContracts = [...contracts];

    if (searchTerm.trim()) {
      updatedContracts = updatedContracts.filter((contract) =>
        (contract.filename || "")
          .toLowerCase()
          .includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== "All") {
      updatedContracts = updatedContracts.filter(
        (contract) =>
          (contract.status || "").toLowerCase() ===
          statusFilter.toLowerCase()
      );
    }

    setFilteredContracts(updatedContracts);
  };

  const getStatusStyle = (status) => {
    if (status === "uploaded") {
      return "bg-emerald-100 text-emerald-700";
    }

    if (status === "failed") {
      return "bg-red-100 text-red-700";
    }

    return "bg-amber-100 text-amber-700";
  };

  const getStatusIcon = (status) => {
    if (status === "uploaded") {
      return <CheckCircle size={16} />;
    }

    if (status === "failed") {
      return <AlertCircle size={16} />;
    }

    return <Clock size={16} />;
  };

  return (
    <Layout>
      <div className="space-y-8">
        <section className="rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-10 text-white shadow-xl">
          <div className="inline-block rounded-full bg-white/10 px-5 py-2 text-sm mb-6">
            Clause Viewer
          </div>

          <h1 className="text-5xl font-bold mb-4">
            Uploaded Contracts
          </h1>

          <p className="max-w-3xl text-lg text-slate-300">
            View uploaded contracts, track processing status, inspect metadata,
            and prepare documents for AI-powered clause analysis.
          </p>
        </section>

        <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h2 className="text-2xl font-bold text-slate-900">
                Contract Library
              </h2>
              <p className="text-sm text-slate-500">
                Search and filter uploaded contract records
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row">
              <div className="relative">
                <Search
                  size={18}
                  className="absolute left-4 top-3.5 text-slate-400"
                />

                <input
                  type="text"
                  placeholder="Search contracts..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-11 pr-4 outline-none focus:border-blue-500 sm:w-72"
                />
              </div>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none focus:border-blue-500"
              >
                <option>All</option>
                <option>uploaded</option>
                <option>failed</option>
                <option>processing</option>
              </select>

              <button
                onClick={fetchContracts}
                className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
              >
                <RefreshCw size={18} />
                Refresh
              </button>
            </div>
          </div>
        </section>

        {loading && (
          <section className="rounded-3xl bg-white p-10 text-center shadow-sm border border-slate-100">
            <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-100 border-t-blue-600"></div>
            <h3 className="text-xl font-bold text-slate-900">
              Loading contracts...
            </h3>
            <p className="text-slate-500">
              Fetching uploaded contract records from backend.
            </p>
          </section>
        )}

        {error && (
          <section className="rounded-3xl border border-red-100 bg-red-50 p-6 text-red-700">
            <div className="flex items-center gap-3">
              <AlertCircle />
              <div>
                <h3 className="font-bold">Unable to load contracts</h3>
                <p>{error}</p>
              </div>
            </div>
          </section>
        )}

        {!loading &&
          filteredContracts.length === 0 &&
          !error && (
            <section className="rounded-3xl bg-white p-12 text-center shadow-sm border border-slate-100">
              <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-blue-50 text-blue-600">
                <FileText size={38} />
              </div>

              <h3 className="text-2xl font-bold text-slate-900">
                No contracts found
              </h3>

              <p className="mt-2 text-slate-500">
                Upload a contract first or adjust your filters.
              </p>
            </section>
          )}

        {!loading &&
          filteredContracts.length > 0 &&
          !error && (
            <section className="grid grid-cols-1 gap-6 xl:grid-cols-2">
              {filteredContracts.map((contract, index) => (
                <div
                  key={contract.contract_id || index}
                  className="rounded-3xl bg-white p-6 shadow-sm border border-slate-100 transition hover:-translate-y-1 hover:shadow-xl"
                >
                  <div className="mb-5 flex items-start justify-between gap-4">
                    <div className="flex items-start gap-4">
                      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-100 text-blue-600">
                        <FileText size={26} />
                      </div>

                      <div>
                        <h3 className="text-xl font-bold text-slate-900">
                          {contract.filename || "Untitled Contract"}
                        </h3>

                        <p className="mt-1 text-sm text-slate-500">
                          Legal document uploaded for AI analysis
                        </p>
                      </div>
                    </div>

                    <span
                      className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-semibold ${getStatusStyle(
                        contract.status
                      )}`}
                    >
                      {getStatusIcon(contract.status)}
                      {contract.status || "Unknown"}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                    <div className="rounded-2xl bg-slate-50 p-4">
                      <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-500">
                        <Hash size={16} />
                        Contract ID
                      </div>

                      <p className="break-all font-bold text-slate-900">
                        {contract.contract_id || "N/A"}
                      </p>
                    </div>

                    <div className="rounded-2xl bg-slate-50 p-4">
                      <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-500">
                        <Calendar size={16} />
                        Upload Time
                      </div>

                      <p className="font-bold text-slate-900">
                        {contract.upload_time
                          ? new Date(
                              contract.upload_time
                            ).toLocaleString()
                          : "N/A"}
                      </p>
                    </div>
                  </div>

                  {contract.error_message && (
                    <div className="mt-4 rounded-2xl bg-red-50 p-4 text-red-700">
                      <div className="mb-1 flex items-center gap-2 font-bold">
                        <AlertCircle size={18} />
                        Error Message
                      </div>

                      <p>{contract.error_message}</p>
                    </div>
                  )}

                  <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                   <button
  onClick={() => navigate("/analyze")}
  className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
>
  <Eye size={18} />
  View Clauses
</button>

<button
  onClick={() => navigate("/analyze")}
  className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-slate-100 px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-200"
>
  Analyze Contract
</button>
                  </div>
                </div>
              ))}
            </section>
          )}
      </div>
    </Layout>
  );
}

export default ClauseViewer;