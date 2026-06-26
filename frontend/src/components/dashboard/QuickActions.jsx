// import { Link } from "react-router-dom";

// function QuickActions() {
//   return (
//     <div className="bg-white rounded-xl shadow-md p-6 mt-8">
//       <h2 className="text-2xl font-bold mb-5">
//         Quick Actions
//       </h2>

//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
//         <Link
//           to="/upload"
//           className="bg-blue-600 text-white text-center py-3 rounded-lg hover:bg-blue-700"
//         >
//           Upload Contract
//         </Link>

//         <Link
//           to="/viewer"
//           className="bg-green-600 text-white text-center py-3 rounded-lg hover:bg-green-700"
//         >
//           Clause Viewer
//         </Link>

//         <Link
//           to="/chatbot"
//           className="bg-purple-600 text-white text-center py-3 rounded-lg hover:bg-purple-700"
//         >
//           Chatbot
//         </Link>

//         <Link
//           to="/analyze"
//           className="bg-orange-600 text-white text-center py-3 rounded-lg hover:bg-orange-700"
//         >
//           Analyze Contract
//         </Link>
//       </div>
//     </div>
//   );
// }

// export default QuickActions;


// recently updated quickactions.jsx file
import { Link } from "react-router-dom";
import {
  UploadCloud,
  FileSearch,
  MessageSquare,
  BarChart3,
} from "lucide-react";

function QuickActions() {
  const actions = [
    {
      title: "Upload Contract",
      description: "Upload a new legal document",
      path: "/upload",
      icon: UploadCloud,
      style: "from-blue-600 to-indigo-600",
    },
    {
      title: "Clause Viewer",
      description: "Review extracted clauses",
      path: "/viewer",
      icon: FileSearch,
      style: "from-emerald-500 to-green-600",
    },
    {
      title: "Chatbot",
      description: "Ask contract questions",
      path: "/chatbot",
      icon: MessageSquare,
      style: "from-purple-600 to-fuchsia-600",
    },
    {
      title: "Analyze Contract",
      description: "Run risk analysis",
      path: "/analyze",
      icon: BarChart3,
      style: "from-orange-500 to-red-500",
    },
  ];

  return (
    <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900">
          Quick Actions
        </h2>
        <p className="text-sm text-slate-500">
          Jump directly into the most used workflows
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
        {actions.map((action, index) => {
          const Icon = action.icon;

          return (
            <Link
              key={index}
              to={action.path}
              className={`group rounded-3xl bg-gradient-to-br ${action.style} p-6 text-white shadow-lg transition hover:-translate-y-1 hover:shadow-2xl`}
            >
              <div className="mb-5 flex h-13 w-13 items-center justify-center rounded-2xl bg-white/20">
                <Icon size={24} />
              </div>

              <h3 className="text-lg font-bold">
                {action.title}
              </h3>

              <p className="mt-1 text-sm text-white/80">
                {action.description}
              </p>

              <div className="mt-5 text-sm font-semibold opacity-90 group-hover:translate-x-1 transition">
                Open →
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}

export default QuickActions;