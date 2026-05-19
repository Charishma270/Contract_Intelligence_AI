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

//     try {
//       const res = await axios.post("http://127.0.0.1:8000/analyze", {
//         query: input, // ✅ FIXED
//       });

//       setResults(res.data);
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
//       <div className="flex gap-2 mb-6 items-end">
        
//         {/* TEXTAREA */}
//         <textarea
//           placeholder="Enter query (e.g. termination clause)"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           rows={1}
//           className="flex-1 border px-3 py-2 rounded resize-none outline-none min-h-[36px] max-h-24 overflow-y-auto"
          
//           /* ✅ Auto height (1 → 4 lines) */
//           onInput={(e) => {
//             e.target.style.height = "auto";
//             e.target.style.height = Math.min(e.target.scrollHeight, 96) + "px";
//           }}

//           /* ✅ Enter + Shift handling */
//           onKeyDown={(e) => {
//             if (e.key === "Enter" && !e.shiftKey) {
//               e.preventDefault();
//               handleAnalyze();
//             }
//           }}
//         />

//         {/* BUTTON (unchanged as you wanted) */}
//         <button
//           onClick={handleAnalyze}
//           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded h-[36px]"
//         >
//           Analyze
//         </button>
//       </div>

//       {/* LOADING */}
//       {loading && <p className="text-blue-600">Analyzing...</p>}

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
//         {results.map((item, index) => (
//           <div
//             key={index}
//             className={`p-4 rounded shadow ${
//               item.risk_level === "High"
//                 ? "bg-red-100"
//                 : item.risk_level === "Medium"
//                 ? "bg-yellow-100"
//                 : "bg-green-100"
//             }`}
//           >
//             <h3 className="font-bold">{item.clause_type}</h3>

//             <p className="text-sm text-gray-700 mb-2">
//               {item.clause_text}
//             </p>

//             <p>Risk: {item.risk_level}</p>
//             <p>
//               Confidence:{" "}
//               {(item.legal_bert_confidence * 100).toFixed(2)}%
//             </p>
//             <p>Similarity: {item.similarity_score}</p>
//             <p>Hybrid Score: {item.hybrid_score}</p>

//             {item.model_disagreement && (
//               <p className="text-red-600 font-semibold mt-2">
//                 ⚠ Model Disagreement Detected
//               </p>
//             )}
//           </div>
//         ))}
//       </div>
//     </Layout>
//   );
// }

// export default Analyze;



//updateddddddddd
// import { useState } from "react";
// import axios from "axios";
// import Layout from "../components/layout/Layout";

// function Analyze() {
//   const [input, setInput] = useState("");
//   const [results, setResults] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [expandedIndex, setExpandedIndex] = useState(null);

//   const handleAnalyze = async () => {
//     if (!input.trim()) return;

//     setLoading(true);

//     try {
//       const res = await axios.post("http://localhost:8000/analyze", {
//         query: input
//       });

//       setResults(res.data);
//     } catch (err) {
//       console.error(err);
//       alert("Error connecting to backend");
//     }

//     setLoading(false);
//   };

//   const toggleExpand = (index) => {
//     setExpandedIndex(expandedIndex === index ? null : index);
//   };

//   return (
//     <Layout>
//       <div className="max-w-6xl mx-auto">

//         {/* PAGE TITLE */}
//         <h2 className="text-3xl font-bold mb-6 text-center">
//           AI Clause Analysis
//         </h2>

//         {/* INPUT SECTION */}
//         <div className="bg-white p-4 rounded-lg shadow mb-6">
//           <div className="flex items-end gap-3">

//             {/* TEXTAREA */}
//             <textarea
//               placeholder="Enter query (e.g. termination clause)"
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               rows={1}
//               className="flex-1 border rounded px-3 py-2 outline-none resize-none min-h-[40px] max-h-28 overflow-y-auto"
//               onInput={(e) => {
//                 e.target.style.height = "auto";
//                 e.target.style.height =
//                   Math.min(e.target.scrollHeight, 112) + "px";
//               }}
//               onKeyDown={(e) => {
//                 if (e.key === "Enter" && !e.shiftKey) {
//                   e.preventDefault();
//                   handleAnalyze();
//                 }
//               }}
//             />

//             {/* BUTTON */}
//             <button
//               onClick={handleAnalyze}
//               className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded h-[42px]"
//             >
//               Analyze
//             </button>

//           </div>
//         </div>

//         {/* LOADING */}
//         {loading && (
//           <div className="text-center text-blue-600 font-semibold mb-4">
//             Analyzing contract...
//           </div>
//         )}

//         {/* RESULTS */}
//         <div className="space-y-5">

//           {results.map((item, index) => (
//             <div
//               key={index}
//               className={`rounded-lg shadow p-5 border-l-8 ${
//                 item.risk_level === "High"
//                   ? "border-red-500 bg-red-50"
//                   : item.risk_level === "Medium"
//                   ? "border-yellow-500 bg-yellow-50"
//                   : "border-green-500 bg-green-50"
//               }`}
//             >

//               {/* TOP SECTION */}
//               <div className="flex justify-between items-start mb-4">

//                 <div>
//                   <h3 className="text-xl font-bold">
//                     {item.clause_type}
//                   </h3>

//                   <p className="text-sm text-gray-600">
//                     Retrieved Label: {item.retrieved_label}
//                   </p>
//                 </div>

//                 {/* RISK BADGE */}
//                 <span
//                   className={`px-3 py-1 rounded-full text-sm font-semibold ${
//                     item.risk_level === "High"
//                       ? "bg-red-500 text-white"
//                       : item.risk_level === "Medium"
//                       ? "bg-yellow-400 text-black"
//                       : "bg-green-500 text-white"
//                   }`}
//                 >
//                   {item.risk_level} Risk
//                 </span>

//               </div>

//               {/* MODEL INFO */}
//               <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">

//                 <div className="bg-white p-3 rounded shadow-sm">
//                   <p className="text-sm text-gray-500">
//                     Legal-BERT Prediction
//                   </p>

//                   <p className="font-semibold">
//                     {item.legal_bert_prediction}
//                   </p>
//                 </div>

//                 <div className="bg-white p-3 rounded shadow-sm">
//                   <p className="text-sm text-gray-500">
//                     Similarity Score
//                   </p>

//                   <p className="font-semibold">
//                     {item.similarity_score}
//                   </p>
//                 </div>

//                 <div className="bg-white p-3 rounded shadow-sm">
//                   <p className="text-sm text-gray-500">
//                     Hybrid Score
//                   </p>

//                   <p className="font-semibold">
//                     {item.hybrid_score}
//                   </p>
//                 </div>

//                 <div className="bg-white p-3 rounded shadow-sm">
//                   <p className="text-sm text-gray-500">
//                     Confidence
//                   </p>

//                   <p className="font-semibold">
//                     {(item.legal_bert_confidence * 100).toFixed(2)}%
//                   </p>
//                 </div>

//               </div>

//               {/* PROGRESS BAR */}
//               <div className="mb-4">
//                 <div className="w-full bg-gray-200 rounded-full h-3">

//                   <div
//                     className="bg-blue-600 h-3 rounded-full"
//                     style={{
//                       width: `${item.legal_bert_confidence * 100}%`
//                     }}
//                   />

//                 </div>
//               </div>

//               {/* DISAGREEMENT WARNING */}
//               {item.model_disagreement && (
//                 <div className="bg-red-100 text-red-700 px-3 py-2 rounded mb-4 font-semibold">
//                   ⚠ Model Disagreement Detected
//                 </div>
//               )}

//               {/* CLAUSE TEXT */}
//               <div className="bg-white rounded p-4 shadow-sm">

//                 <div className="flex justify-between items-center mb-2">

//                   <h4 className="font-semibold">
//                     Clause Text
//                   </h4>

//                   <button
//                     onClick={() => toggleExpand(index)}
//                     className="text-blue-600 text-sm"
//                   >
//                     {expandedIndex === index
//                       ? "Show Less"
//                       : "Show More"}
//                   </button>

//                 </div>

//                 <p className="text-gray-700 text-sm">
//                   {expandedIndex === index
//                     ? item.clause_text
//                     : item.clause_text.slice(0, 200) + "..."}
//                 </p>

//               </div>

//             </div>
//           ))}

//         </div>
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







// ultra updateddddddddd

import { useState } from "react";
import Layout from "../components/layout/Layout";

function Analyze() {
  const [input, setInput] = useState("");
  const [expandedIndex, setExpandedIndex] = useState(null);

  // MOCK DATA (temporary until backend works)
  const mockResults = [
    {
      clause_type: "Termination Clause",
      retrieved_label: "Contract Termination",
      legal_bert_prediction: "Termination",
      legal_bert_confidence: 0.97,
      risk_level: "High",
      similarity_score: 0.69,
      hybrid_score: 0.83,
      model_disagreement: true,
      clause_text:
        "Either party may terminate this agreement immediately upon breach of contract or failure to meet obligations within 30 days of notice.",
    },
    {
      clause_type: "Confidentiality Clause",
      retrieved_label: "Confidentiality",
      legal_bert_prediction: "Confidentiality",
      legal_bert_confidence: 0.89,
      risk_level: "Medium",
      similarity_score: 0.74,
      hybrid_score: 0.79,
      model_disagreement: false,
      clause_text:
        "All confidential information shared between parties shall remain protected and cannot be disclosed without prior written consent.",
    },
    {
      clause_type: "Payment Clause",
      retrieved_label: "Payment Terms",
      legal_bert_prediction: "Payment",
      legal_bert_confidence: 0.81,
      risk_level: "Low",
      similarity_score: 0.77,
      hybrid_score: 0.75,
      model_disagreement: false,
      clause_text:
        "Payment shall be completed within 15 business days after invoice generation.",
    },
  ];

  return (
    <Layout>
      <div className="max-w-7xl mx-auto py-8">
        <h1 className="text-5xl font-bold text-center mb-10">
          AI Clause Analysis
        </h1>

        {/* INPUT */}
        <div className="bg-white rounded-xl shadow-md p-4 mb-8 flex gap-3 items-end">
          <textarea
            placeholder="Enter query (e.g. termination clause)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={1}
            className="flex-1 border rounded-lg px-4 py-3 resize-none outline-none min-h-[50px] max-h-[140px] overflow-y-auto"
            onInput={(e) => {
              e.target.style.height = "auto";
              e.target.style.height =
                Math.min(e.target.scrollHeight, 140) + "px";
            }}
          />

          <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold">
            Analyze
          </button>
        </div>

        {/* RESULTS */}
        <div className="space-y-6">
          {mockResults.map((item, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-md p-6"
            >
              {/* TOP */}
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">
                  {item.clause_type}
                </h2>

                <span
                  className={`px-4 py-2 rounded-full text-sm font-semibold ${
                    item.risk_level === "High"
                      ? "bg-red-100 text-red-600"
                      : item.risk_level === "Medium"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-green-100 text-green-700"
                  }`}
                >
                  {item.risk_level} Risk
                </span>
              </div>

              {/* DETAILS */}
              <div className="grid md:grid-cols-2 gap-3 mb-5">
                <p>
                  <strong>Retrieved Label:</strong>{" "}
                  {item.retrieved_label}
                </p>

                <p>
                  <strong>Transformer Prediction:</strong>{" "}
                  {item.legal_bert_prediction}
                </p>

                <p>
                  <strong>Similarity Score:</strong>{" "}
                  {item.similarity_score}
                </p>

                <p>
                  <strong>Hybrid Score:</strong>{" "}
                  {item.hybrid_score}
                </p>
              </div>

              {/* CONFIDENCE */}
              <div className="mb-5">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">
                    Confidence Score
                  </span>

                  <span className="font-bold text-blue-600">
                    {(item.legal_bert_confidence * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-600"
                    style={{
                      width: `${
                        item.legal_bert_confidence * 100
                      }%`,
                    }}
                  />
                </div>
              </div>

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
                  {expandedIndex === index
                    ? item.clause_text
                    : item.clause_text.slice(0, 100) + "..."}
                </p>

                <button
                  className="text-blue-600 mt-3 font-semibold"
                  onClick={() =>
                    setExpandedIndex(
                      expandedIndex === index
                        ? null
                        : index
                    )
                  }
                >
                  {expandedIndex === index
                    ? "Show Less"
                    : "Read More"}
                </button>
              </div>
            </div>
          ))}
        </div>
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