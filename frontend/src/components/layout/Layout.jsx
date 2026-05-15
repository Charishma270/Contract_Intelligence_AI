import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

// function Layout({ children }) {
//   return (
//     <div className="flex">
//       <Sidebar />

//       <div className="flex-1">
//         <Navbar />

//         <div className="p-6 bg-gray-100 min-h-screen">
//           {children}
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Layout;

// function Layout({ children }) {
//   return (
//     <div className="flex">
//       <Sidebar />

//       <div className="flex-1">
//         <Navbar />

//         {/* KEEP THIS */}
//         <div className="p-6 bg-gray-100 min-h-screen">
//           {children}
//         </div>
//       </div>
//     </div>
//   );
// }


function Layout({ children, fullWidth = false }) {
  return (
    <div className="flex">
      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <div
          className={`bg-gray-100 min-h-screen ${
            fullWidth ? "" : "p-6"
          }`}
        >
          {children}
        </div>
      </div>
    </div>
  );
}

export default Layout;