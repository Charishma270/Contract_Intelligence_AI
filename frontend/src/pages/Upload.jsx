// import Layout from "../components/layout/Layout";
// import { useState } from "react";

// function Upload() {
//   const [file, setFile] = useState(null);

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//   };

//   const handleUpload = () => {
//     if (!file) return alert("Please select a file");

//     console.log("Uploading:", file.name);
    
//   };

//   return (
//     <Layout>
//       <h2 className="text-2xl font-bold mb-6">Upload Contract</h2>

//       <div className="bg-white p-6 rounded shadow w-full max-w-xl">
        
//         <input
//           type="file"
//           accept=".pdf,.doc,.docx"
//           onChange={handleFileChange}
//           className="mb-4"
//         />

//         {file && (
//           <p className="text-sm text-gray-600 mb-4">
//             Selected: {file.name}
//           </p>
//         )}

//         <button
//           onClick={handleUpload}
//           className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//         >
//           Upload
//         </button>

//       </div>
//     </Layout>
//   );
// }

// export default Upload;


// week 3 wedddd
// import Layout from "../components/layout/Layout";
// import { useState } from "react";
// import { uploadContract } from "../services/api";

// function Upload() {
//   const [file, setFile] = useState(null);
//   const [uploading, setUploading] = useState(false);
//   const [message, setMessage] = useState("");
//   const [error, setError] = useState("");

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//     setMessage("");
//     setError("");
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       setError("Please select a file first.");
//       return;
//     }

//     setUploading(true);
//     setMessage("");
//     setError("");

//     try {
//       const data = await uploadContract(file);

//       console.log("Upload response:", data);

//       setMessage("Contract uploaded successfully.");
//       setFile(null);
//     } catch (err) {
//       console.log("Upload error:", err);

//       setError("Upload failed. Please check backend connection.");
//     } finally {
//       setUploading(false);
//     }
//   };

//   return (
//     <Layout>
//       <h2 className="text-2xl font-bold mb-6">Upload Contract</h2>

//       <div className="bg-white p-6 rounded shadow w-full max-w-xl">
//         <input
//           type="file"
//           accept=".pdf,.doc,.docx"
//           onChange={handleFileChange}
//           className="mb-4"
//         />

//         {file && (
//           <p className="text-sm text-gray-600 mb-4">
//             Selected: {file.name}
//           </p>
//         )}

//         {message && (
//           <div className="bg-green-100 text-green-700 px-4 py-3 rounded mb-4">
//             {message}
//           </div>
//         )}

//         {error && (
//           <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-4">
//             {error}
//           </div>
//         )}

//         <button
//           onClick={handleUpload}
//           disabled={uploading}
//           className={`text-white px-4 py-2 rounded ${
//             uploading
//               ? "bg-gray-400 cursor-not-allowed"
//               : "bg-blue-600 hover:bg-blue-700"
//           }`}
//         >
//           {uploading ? "Uploading..." : "Upload"}
//         </button>
//       </div>
//     </Layout>
//   );
// }

// export default Upload;


// week 3 wedddddddddddddddd

import Layout from "../components/layout/Layout";
import { useState } from "react";
import { uploadContract } from "../services/api";

function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [uploadResult, setUploadResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setError("");
    setUploadResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setUploading(true);
    setMessage("");
    setError("");
    setUploadResult(null);

    try {
      const data = await uploadContract(file);

      console.log("Upload response:", data);

      setMessage("Contract uploaded successfully.");
      setUploadResult(data);
      setFile(null);
    } catch (err) {
      console.log("Upload error:", err);

      setError("Upload failed. Please check backend connection.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-6">Upload Contract</h2>

      <div className="bg-white p-6 rounded shadow w-full max-w-xl">
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
          className="mb-4"
        />

        {file && (
          <p className="text-sm text-gray-600 mb-4">
            Selected: {file.name}
          </p>
        )}

        {message && (
          <div className="bg-green-100 text-green-700 px-4 py-3 rounded mb-4">
            {message}
          </div>
        )}

        {uploadResult && (
          <div className="bg-gray-100 rounded p-4 mb-4 text-sm text-gray-700 space-y-2">
            <p>
              <strong>Contract ID:</strong>{" "}
              {uploadResult.contract_id || "N/A"}
            </p>

            <p>
              <strong>Filename:</strong>{" "}
              {uploadResult.filename || "N/A"}
            </p>

            <p>
              <strong>Status:</strong>{" "}
              {uploadResult.status || "N/A"}
            </p>

            <p>
              <strong>Message:</strong>{" "}
              {uploadResult.message || "N/A"}
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={uploading}
          className={`text-white px-4 py-2 rounded ${
            uploading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </div>
    </Layout>
  );
}

export default Upload;