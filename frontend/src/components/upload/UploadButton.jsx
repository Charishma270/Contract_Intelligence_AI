import { Upload } from "lucide-react";

function UploadButton() {
  return (
    <div className="flex justify-end">

      <button className="flex items-center gap-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-4 rounded-2xl font-semibold shadow-lg transition">

        <Upload size={20} />

        Upload & Analyze

      </button>

    </div>
  );
}

export default UploadButton;