// import Sidebar from "./Sidebar";
// import Navbar from "./Navbar";

// function Layout({ children, fullWidth = false }) {
//   return (
//     <div className="flex">
//       <Sidebar />

//       <div className="flex-1">
//         <Navbar />

//         <div
//           className={`bg-gray-100 min-h-screen ${
//             fullWidth ? "" : "p-6"
//           }`}
//         >
//           {children}
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Layout;


//recently updated layout.jsx file
// import Sidebar from "./Sidebar";
// import Navbar from "./Navbar";

// function Layout({ children, fullWidth = false }) {
//   return (
//     <div className="flex min-h-screen bg-slate-100">
//       <Sidebar />

//       <div className="flex-1 min-w-0">
//         <Navbar />

//         <main
//           className={`min-h-screen ${
//             fullWidth ? "" : "px-6 py-6 lg:px-8"
//           }`}
//         >
//           {children}
//         </main>
//       </div>
//     </div>
//   );
// }

// export default Layout;


// changes 2

import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout({ children, fullWidth = false }) {
  return (
    <div className="flex min-h-screen bg-slate-100 dark:bg-slate-950">
      <Sidebar />

      <div className="flex-1 min-w-0">
        <Navbar />

        <main
          className={`min-h-screen ${
            fullWidth ? "" : "px-6 py-6 lg:px-8"
          }`}
        >
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;