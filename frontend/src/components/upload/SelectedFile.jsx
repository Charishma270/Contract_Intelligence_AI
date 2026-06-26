import { FileText, X } from "lucide-react";

function SelectedFile() {
  return (
    <div className="bg-white rounded-3xl shadow-lg p-8">

      <h2 className="text-2xl font-bold mb-6">
        Selected File
      </h2>

      <div className="flex justify-between items-center bg-slate-50 rounded-2xl p-5">

        <div className="flex items-center gap-5">

          <div className="w-14 h-14 rounded-xl bg-blue-100 flex items-center justify-center">

            <FileText className="text-blue-600"/>

          </div>

          <div>

            <h3 className="font-semibold">
              Employment_Agreement.pdf
            </h3>

            <p className="text-gray-500">
              2.4 MB
            </p>

          </div>

        </div>

        <button>

          <X className="text-red-500"/>

        </button>

      </div>

    </div>
  );
}

export default SelectedFile;