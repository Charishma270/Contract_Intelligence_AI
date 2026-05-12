import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white p-5">
      <h2 className="text-xl font-bold mb-6">Contract AI</h2>

      <nav className="flex flex-col gap-4">
        <Link to="/dashboard" className="hover:text-blue-400">
          Dashboard
        </Link>

        <Link to="/upload" className="hover:text-blue-400">
          Upload Contract
        </Link>

        <Link to="/viewer" className="hover:text-blue-400">
          Clause Viewer
        </Link>

        <Link to="/chat" className="hover:text-blue-400">
          Chatbot
        </Link>
      </nav>
    </div>
  );
}

export default Sidebar;