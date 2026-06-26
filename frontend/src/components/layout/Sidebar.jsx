//impppppppppppppppppppp

// import { Link } from "react-router-dom";

// function Sidebar() {
//   return (
//     <div className="w-64 h-screen bg-gray-900 text-white p-5">
//       <h2 className="text-xl font-bold mb-6">Contract AI</h2>

//       <nav className="flex flex-col gap-4">
//         <Link to="/dashboard" className="hover:text-blue-400">
//           Dashboard
//         </Link>

//         <Link to="/upload" className="hover:text-blue-400">
//           Upload Contract
//         </Link>

//         <Link to="/viewer" className="hover:text-blue-400">
//           Clause Viewer
//         </Link>

//         <Link to="/chatbot" className="hover:text-blue-400">
//           Chatbot
//         </Link>

//         <Link to="/analyze" className="hover:text-blue-400">
//           Analyze
//         </Link>
        
//       </nav>
//     </div>
//   );
// }

// export default Sidebar;



// recently updated sidebar.jsx file

import {
  LayoutDashboard,
  Upload,
  FileText,
  MessageSquare,
  Search,
  ShieldCheck,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menu = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    name: "Upload Contract",
    icon: Upload,
    path: "/upload",
  },
  {
    name: "Clause Viewer",
    icon: FileText,
    path: "/viewer",
  },
  {
    name: "Chatbot",
    icon: MessageSquare,
    path: "/chatbot",
  },
  {
    name: "Analyze",
    icon: Search,
    path: "/analyze",
  },
];

function Sidebar() {
  return (
    <aside className="w-72 min-h-screen bg-[#0f172a] text-white flex flex-col shadow-2xl">

      <div className="px-8 py-8 border-b border-slate-700">

        <div className="flex items-center gap-3">

          <div className="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center">

            <ShieldCheck size={24} />

          </div>

          <div>

            <h1 className="font-bold text-xl">
              Contract AI
            </h1>

            <p className="text-xs text-slate-400">
              Legal Intelligence
            </p>

          </div>

        </div>

      </div>

      <nav className="flex-1 mt-8 px-4">

        {menu.map((item) => {

          const Icon = item.icon;

          return (

            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-4 px-5 py-4 rounded-xl mb-3 transition-all duration-300
                ${
                  isActive
                    ? "bg-blue-600 shadow-lg"
                    : "hover:bg-slate-800 text-slate-300"
                }`
              }
            >
              <Icon size={20} />

              <span>{item.name}</span>

            </NavLink>

          );
        })}

      </nav>

      <div className="border-t border-slate-700 p-6">

        <div className="flex items-center gap-3">

          <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-lg font-bold">

            M

          </div>

          <div>

            <h3 className="font-semibold">
              Mukt Patel
            </h3>

            <p className="text-xs text-slate-400">
              Frontend Developer
            </p>

          </div>

        </div>

      </div>

    </aside>
  );
}

export default Sidebar;