import { UploadCloud } from "lucide-react";

function DropZone() {
  return (
    <div className="bg-white rounded-3xl shadow-lg p-10">

      <div className="border-2 border-dashed border-blue-300 rounded-2xl p-16 flex flex-col items-center justify-center hover:bg-blue-50 transition">

        <UploadCloud
          size={70}
          className="text-blue-600 mb-5"
        />

        <h2 className="text-2xl font-bold mb-2">
          Drag & Drop Contract
        </h2>

        <p className="text-gray-500 mb-6">
          PDF, DOCX (Maximum 20 MB)
        </p>

        <button className="bg-blue-600 hover:bg-blue-700 text-white px-7 py-3 rounded-xl font-semibold transition">

          Browse Files

        </button>

      </div>

    </div>
  );
}

export default DropZone;