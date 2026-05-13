import Layout from "../components/layout/Layout";
import { useState } from "react";

function Upload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!file) return alert("Please select a file");

    console.log("Uploading:", file.name);
    
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

        <button
          onClick={handleUpload}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Upload
        </button>

      </div>
    </Layout>
  );
}

export default Upload;