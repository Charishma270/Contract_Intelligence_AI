import { Link } from "react-router-dom";

function QuickActions() {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">
      <h2 className="text-2xl font-bold mb-5">
        Quick Actions
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link
          to="/upload"
          className="bg-blue-600 text-white text-center py-3 rounded-lg hover:bg-blue-700"
        >
          Upload Contract
        </Link>

        <Link
          to="/viewer"
          className="bg-green-600 text-white text-center py-3 rounded-lg hover:bg-green-700"
        >
          Clause Viewer
        </Link>

        <Link
          to="/chatbot"
          className="bg-purple-600 text-white text-center py-3 rounded-lg hover:bg-purple-700"
        >
          Chatbot
        </Link>

        <Link
          to="/analyze"
          className="bg-orange-600 text-white text-center py-3 rounded-lg hover:bg-orange-700"
        >
          Analyze Contract
        </Link>
      </div>
    </div>
  );
}

export default QuickActions;