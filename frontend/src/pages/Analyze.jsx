// import { useState } from "react";
// import axios from "axios";
// import Layout from "../components/layout/Layout";

// function Analyze() {
//   const [input, setInput] = useState("");
//   const [results, setResults] = useState([]);
//   const [loading, setLoading] = useState(false);

//   const handleAnalyze = async () => {
//     if (!input.trim()) return;

//     setLoading(true);
//     setResults([]); // clear previous results

//     try {
//       const res = await axios.post("http://localhost:8000/analyze", {
//         user_query: input
//       });

//       setResults(res.data || []);
//     } catch (err) {
//       console.error(err);
//       alert("Error connecting to backend");
//     }

//     setLoading(false);
//     setInput("");
//   };

//   return (
//     <Layout>
//       <h2 className="text-2xl font-bold mb-4">Clause Analysis</h2>

//       {/* INPUT */}
//       <div className="flex gap-2 mb-6">
//         <input
//           type="text"
//           placeholder="Enter query (e.g. termination clause)"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           className="flex-1 border px-3 py-2 rounded outline-none"
//         />

//         <button
//           onClick={handleAnalyze}
//           disabled={loading}
//           className="bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
//         >
//           {loading ? "Analyzing..." : "Analyze"}
//         </button>
//       </div>

//       {/* EMPTY STATE */}
//       {!loading && results.length === 0 && (
//         <p className="text-gray-500">No results yet. Try a query.</p>
//       )}

//       {/* RESULTS */}
//       <div className="space-y-4">
//         {results.map((item, index) => {
//           const confidence = item.legal_bert_confidence
//             ? (item.legal_bert_confidence * 100).toFixed(2)
//             : "N/A";

//           return (
//             <div
//               key={index}
//               className={`p-4 rounded shadow ${
//                 item.risk_level === "High"
//                   ? "bg-red-100"
//                   : item.risk_level === "Medium"
//                   ? "bg-yellow-100"
//                   : "bg-green-100"
//               }`}
//             >
//               <h3 className="font-bold text-lg">{item.clause_type}</h3>

//               <p className="text-sm text-gray-700 mb-2">
//                 {item.clause_text}
//               </p>

//               <p><strong>Risk:</strong> {item.risk_level || "N/A"}</p>
//               <p><strong>Confidence:</strong> {confidence}%</p>
//               <p><strong>Similarity:</strong> {item.similarity_score ?? "N/A"}</p>
//               <p><strong>Hybrid Score:</strong> {item.hybrid_score ?? "N/A"}</p>

//               {item.model_disagreement && (
//                 <p className="text-red-600 font-semibold mt-2">
//                   ⚠ Model Disagreement Detected
//                 </p>
//               )}
//             </div>
//           );
//         })}
//       </div>
//     </Layout>
//   );
// }

// export default Analyze;



import { useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";

function Analyze() {
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!input.trim()) return;

    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze", {
        query: input, // ✅ FIXED
      });

      setResults(res.data);
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-4">Clause Analysis</h2>

      {/* INPUT */}
      <div className="flex gap-2 mb-6 items-end">
        
        {/* TEXTAREA */}
        <textarea
          placeholder="Enter query (e.g. termination clause)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={1}
          className="flex-1 border px-3 py-2 rounded resize-none outline-none min-h-[36px] max-h-24 overflow-y-auto"
          
          /* ✅ Auto height (1 → 4 lines) */
          onInput={(e) => {
            e.target.style.height = "auto";
            e.target.style.height = Math.min(e.target.scrollHeight, 96) + "px";
          }}

          /* ✅ Enter + Shift handling */
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleAnalyze();
            }
          }}
        />

        {/* BUTTON (unchanged as you wanted) */}
        <button
          onClick={handleAnalyze}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded h-[36px]"
        >
          Analyze
        </button>
      </div>

      {/* LOADING */}
      {loading && <p className="text-blue-600">Analyzing...</p>}

      {/* EMPTY STATE */}
      {!loading && results.length === 0 && (
        <p className="text-gray-500">No results yet. Try a query.</p>
      )}

      {/* RESULTS */}
      <div className="space-y-4">
        {results.map((item, index) => (
          <div
            key={index}
            className={`p-4 rounded shadow ${
              item.risk_level === "High"
                ? "bg-red-100"
                : item.risk_level === "Medium"
                ? "bg-yellow-100"
                : "bg-green-100"
            }`}
          >
            <h3 className="font-bold">{item.clause_type}</h3>

            <p className="text-sm text-gray-700 mb-2">
              {item.clause_text}
            </p>

            <p>Risk: {item.risk_level}</p>
            <p>
              Confidence:{" "}
              {(item.legal_bert_confidence * 100).toFixed(2)}%
            </p>
            <p>Similarity: {item.similarity_score}</p>
            <p>Hybrid Score: {item.hybrid_score}</p>

            {item.model_disagreement && (
              <p className="text-red-600 font-semibold mt-2">
                ⚠ Model Disagreement Detected
              </p>
            )}
          </div>
        ))}
      </div>
    </Layout>
  );
}

export default Analyze;