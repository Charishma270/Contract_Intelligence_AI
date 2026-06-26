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
// imppppppppppppppp 26-6-26
// import Layout from "../components/layout/Layout";
// import { useState } from "react";
// import { uploadContract } from "../services/api";

// function Upload() {
//   const [file, setFile] = useState(null);
//   const [uploading, setUploading] = useState(false);
//   const [message, setMessage] = useState("");
//   const [error, setError] = useState("");
//   const [uploadResult, setUploadResult] = useState(null);

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//     setMessage("");
//     setError("");
//     setUploadResult(null);
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       setError("Please select a file first.");
//       return;
//     }

//     setUploading(true);
//     setMessage("");
//     setError("");
//     setUploadResult(null);

//     try {
//       const data = await uploadContract(file);

//       console.log("Upload response:", data);

//       setMessage("Contract uploaded successfully.");
//       setUploadResult(data);
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

//         {uploadResult && (
//           <div className="bg-gray-100 rounded p-4 mb-4 text-sm text-gray-700 space-y-2">
//             <p>
//               <strong>Contract ID:</strong>{" "}
//               {uploadResult.contract_id || "N/A"}
//             </p>

//             <p>
//               <strong>Filename:</strong>{" "}
//               {uploadResult.filename || "N/A"}
//             </p>

//             <p>
//               <strong>Status:</strong>{" "}
//               {uploadResult.status || "N/A"}
//             </p>

//             <p>
//               <strong>Message:</strong>{" "}
//               {uploadResult.message || "N/A"}
//             </p>
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



// changes 

// import Layout from "../components/layout/Layout";

// import UploadHero from "../components/upload/UploadHero";
// import DropZone from "../components/upload/DropZone";
// import SelectedFile from "../components/upload/SelectedFile";
// import AIOptions from "../components/upload/AIOptions";
// import UploadProgress from "../components/upload/UploadProgress";
// import UploadButton from "../components/upload/UploadButton";

// function Upload() {
//   return (
//     <Layout>
//       <div className="space-y-8">

//         <UploadHero />

//         <DropZone />

//         <SelectedFile />

//         <UploadProgress />

//         <AIOptions />

//         <UploadButton />

//       </div>
//     </Layout>
//   );
// }

// export default Upload;


// changes 2

import { useState } from "react";
import Layout from "../components/layout/Layout";
import { uploadContract } from "../services/api";
import {
  UploadCloud,
  FileText,
  X,
  CheckCircle,
  AlertCircle,
  Loader2,
} from "lucide-react";

function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (!selectedFile) return;

    setFile(selectedFile);
    setResponse(null);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    try {
      setUploading(true);
      setError("");
      setResponse(null);

      const data = await uploadContract(file);
      setResponse(data);
    } catch (err) {
      console.error("Upload error:", err);
      setError("Upload failed. Please check backend connection.");
    } finally {
      setUploading(false);
    }
  };

  const removeFile = () => {
    setFile(null);
    setResponse(null);
    setError("");
  };

  return (
    <Layout>
      <div className="space-y-8">
        <section className="rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-10 text-white shadow-xl">
          <div className="inline-block rounded-full bg-white/10 px-5 py-2 text-sm mb-6">
            AI Document Upload
          </div>

          <h1 className="text-5xl font-bold mb-4">
            Upload Contract
          </h1>

          <p className="text-lg text-slate-300 max-w-3xl">
            Securely upload legal contracts for AI-powered clause detection,
            risk analysis, entity extraction, and intelligent document review.
          </p>
        </section>

        <section className="bg-white rounded-3xl shadow-lg p-10">
          <label className="block cursor-pointer">
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              className="hidden"
            />

            <div className="border-2 border-dashed border-blue-300 rounded-2xl p-16 flex flex-col items-center justify-center hover:bg-blue-50 transition">
              <UploadCloud size={70} className="text-blue-600 mb-5" />

              <h2 className="text-2xl font-bold mb-2">
                Drag & Drop Contract
              </h2>

              <p className="text-gray-500 mb-6">
                PDF, DOCX, DOC supported
              </p>

              <span className="bg-blue-600 hover:bg-blue-700 text-white px-7 py-3 rounded-xl font-semibold transition">
                Browse Files
              </span>
            </div>
          </label>
        </section>

        {file && (
          <section className="bg-white rounded-3xl shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">
              Selected File
            </h2>

            <div className="flex justify-between items-center bg-slate-50 rounded-2xl p-5">
              <div className="flex items-center gap-5">
                <div className="w-14 h-14 rounded-xl bg-blue-100 flex items-center justify-center">
                  <FileText className="text-blue-600" />
                </div>

                <div>
                  <h3 className="font-semibold">
                    {file.name}
                  </h3>

                  <p className="text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>

              <button onClick={removeFile}>
                <X className="text-red-500" />
              </button>
            </div>
          </section>
        )}

        {uploading && (
          <section className="bg-white rounded-3xl shadow-lg p-8">
            <div className="flex items-center gap-3 mb-4">
              <Loader2 className="animate-spin text-blue-600" />
              <h2 className="text-xl font-bold">
                Uploading and processing...
              </h2>
            </div>

            <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
              <div className="bg-blue-600 h-full rounded-full animate-pulse w-3/4"></div>
            </div>
          </section>
        )}

        {response && (
          <section className="bg-green-50 border border-green-100 rounded-3xl p-6 text-green-700">
            <div className="flex items-start gap-3">
              <CheckCircle />

              <div>
                <h3 className="font-bold text-lg">
                  Contract uploaded successfully
                </h3>

                <p>
                  <strong>Contract ID:</strong>{" "}
                  {response.contract_id || "N/A"}
                </p>

                <p>
                  <strong>Filename:</strong>{" "}
                  {response.filename || file?.name}
                </p>

                <p>
                  <strong>Status:</strong>{" "}
                  {response.status || "Uploaded"}
                </p>

                <p>
                  <strong>Message:</strong>{" "}
                  {response.message || "File uploaded successfully."}
                </p>
              </div>
            </div>
          </section>
        )}

        {error && (
          <section className="bg-red-50 border border-red-100 rounded-3xl p-6 text-red-700">
            <div className="flex items-center gap-3">
              <AlertCircle />
              <p className="font-semibold">{error}</p>
            </div>
          </section>
        )}

        <section className="bg-white rounded-3xl shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">
            AI Processing Options
          </h2>

          <div className="grid md:grid-cols-2 gap-5">
            {[
              "Clause Detection",
              "Risk Analysis",
              "Entity Extraction",
              "AI Summary",
            ].map((item, index) => (
              <label
                key={index}
                className="flex items-center gap-4 p-5 rounded-2xl bg-slate-50 hover:bg-blue-50 cursor-pointer"
              >
                <input type="checkbox" defaultChecked className="w-5 h-5" />
                <span className="font-medium">{item}</span>
              </label>
            ))}
          </div>
        </section>

        <div className="flex justify-end">
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="flex items-center gap-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-500 text-white px-8 py-4 rounded-2xl font-semibold shadow-lg transition"
          >
            {uploading ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                Uploading...
              </>
            ) : (
              <>
                <UploadCloud size={20} />
                Upload & Analyze
              </>
            )}
          </button>
        </div>
      </div>
    </Layout>
  );
}

export default Upload;