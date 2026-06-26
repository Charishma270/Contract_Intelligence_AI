//imppppppppppppp

// function Navbar() {
//   return (
//     <div className="h-16 bg-white shadow flex items-center justify-between px-6">
//       <h1 className="text-lg font-semibold">Dashboard</h1>

//       <div className="flex items-center gap-4">
//         <span className="text-sm text-gray-600">User</span>
//         <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
//       </div>
//     </div>
//   );
// }

// export default Navbar;



// recently changes in navbar.jsx file

// import {
//   Bell,
//   Search,
//   Moon,
// } from "lucide-react";

// function Navbar() {
//   return (
//     <header className="h-20 bg-white border-b flex items-center justify-between px-10 sticky top-0 z-50">

//       <div>

//         <h1 className="text-2xl font-bold">
//           Dashboard
//         </h1>

//         <p className="text-gray-500 text-sm">
//           Welcome back to Contract Intelligence AI
//         </p>

//       </div>

//       <div className="flex items-center gap-5">

//         <div className="relative">

//           <Search
//             size={18}
//             className="absolute left-4 top-3 text-gray-400"
//           />

//           <input
//             type="text"
//             placeholder="Search..."
//             className="pl-11 pr-4 py-2 w-72 rounded-xl border bg-gray-50 outline-none focus:ring-2 focus:ring-blue-500"
//           />

//         </div>

//         <button className="w-11 h-11 rounded-xl bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center">

//           <Bell size={20} />

//         </button>

//         <button className="w-11 h-11 rounded-xl bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center">

//           <Moon size={20} />

//         </button>

//         <div className="flex items-center gap-3">

//           <div className="text-right">

//             <h3 className="font-semibold">
//               Mukt Patel
//             </h3>

//             <p className="text-sm text-gray-500">
//               Frontend Developer
//             </p>

//           </div>

//           <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">

//             M

//           </div>

//         </div>

//       </div>

//     </header>
//   );
// }

// export default Navbar;


// changes no. 2

// import { useEffect, useRef, useState } from "react";
// import {
//   Bell,
//   Search,
//   Moon,
//   User,
//   Settings,
//   LogOut,
//   ChevronDown,
// } from "lucide-react";
// import { useNavigate } from "react-router-dom";

// function Navbar() {
//   const [openProfile, setOpenProfile] = useState(false);
//   const dropdownRef = useRef(null);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const handleClickOutside = (e) => {
//       if (
//         dropdownRef.current &&
//         !dropdownRef.current.contains(e.target)
//       ) {
//         setOpenProfile(false);
//       }
//     };

//     document.addEventListener("mousedown", handleClickOutside);

//     return () => {
//       document.removeEventListener(
//         "mousedown",
//         handleClickOutside
//       );
//     };
//   }, []);

//   const handleLogout = () => {
//     setOpenProfile(false);
//     navigate("/login");
//   };

//   return (
//     <header className="h-20 bg-white border-b flex items-center justify-between px-10 sticky top-0 z-50">
//       <div>
//         <h1 className="text-2xl font-bold">Dashboard</h1>

//         <p className="text-gray-500 text-sm">
//           Welcome back to Contract Intelligence AI
//         </p>
//       </div>

//       <div className="flex items-center gap-5">
//         <div className="relative">
//           <Search
//             size={18}
//             className="absolute left-4 top-3 text-gray-400"
//           />

//           <input
//             type="text"
//             placeholder="Search..."
//             className="pl-11 pr-4 py-2 w-72 rounded-xl border bg-gray-50 outline-none focus:ring-2 focus:ring-blue-500"
//           />
//         </div>

//         <button className="w-11 h-11 rounded-xl bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center">
//           <Bell size={20} />
//         </button>

//         <button className="w-11 h-11 rounded-xl bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center">
//           <Moon size={20} />
//         </button>

//         <div className="relative" ref={dropdownRef}>
//           <button
//             onClick={() => setOpenProfile(!openProfile)}
//             className="flex items-center gap-3 rounded-2xl px-3 py-2 hover:bg-gray-100 transition"
//           >
//             <div className="text-right">
//               <h3 className="font-semibold">Mukt Patel</h3>

//               <p className="text-sm text-gray-500">
//                 Frontend Developer
//               </p>
//             </div>

//             <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
//               M
//             </div>

//             <ChevronDown
//               size={18}
//               className={`text-gray-500 transition ${
//                 openProfile ? "rotate-180" : ""
//               }`}
//             />
//           </button>

//           {openProfile && (
//             <div className="absolute right-0 mt-3 w-64 rounded-2xl bg-white border shadow-2xl p-3 z-50">
//               <div className="px-4 py-3 border-b">
//                 <h3 className="font-bold text-gray-900">
//                   Mukt Patel
//                 </h3>
//                 <p className="text-sm text-gray-500">
//                   Frontend Developer
//                 </p>
//               </div>

//               <button className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition">
//                 <User size={18} />
//                 <span>My Profile</span>
//               </button>

//               <button className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition">
//                 <Settings size={18} />
//                 <span>Settings</span>
//               </button>

//               <button className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition">
//                 <Moon size={18} />
//                 <span>Dark Mode</span>
//               </button>

//               <button
//                 onClick={handleLogout}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl text-red-600 hover:bg-red-50 transition"
//               >
//                 <LogOut size={18} />
//                 <span>Logout</span>
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </header>
//   );
// }

// export default Navbar;


// changes no. 3

// import { useEffect, useRef, useState } from "react";
// import {
//   Bell,
//   Search,
//   Moon,
//   Sun,
//   User,
//   Settings,
//   LogOut,
//   ChevronDown,
// } from "lucide-react";
// import { useNavigate } from "react-router-dom";

// function Navbar() {
//   const [openProfile, setOpenProfile] = useState(false);
//   const [darkMode, setDarkMode] = useState(false);

//   const dropdownRef = useRef(null);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const savedTheme = localStorage.getItem("theme");

//     if (savedTheme === "dark") {
//       document.documentElement.classList.add("dark");
//       setDarkMode(true);
//     }
//   }, []);

//   const toggleDarkMode = () => {
//     const newMode = !darkMode;
//     setDarkMode(newMode);

//     if (newMode) {
//       document.documentElement.classList.add("dark");
//       localStorage.setItem("theme", "dark");
//     } else {
//       document.documentElement.classList.remove("dark");
//       localStorage.setItem("theme", "light");
//     }
//   };

//   useEffect(() => {
//     const handleClickOutside = (e) => {
//       if (
//         dropdownRef.current &&
//         !dropdownRef.current.contains(e.target)
//       ) {
//         setOpenProfile(false);
//       }
//     };

//     document.addEventListener("mousedown", handleClickOutside);

//     return () => {
//       document.removeEventListener("mousedown", handleClickOutside);
//     };
//   }, []);

//   const handleLogout = () => {
//     setOpenProfile(false);
//     navigate("/login");
//   };

//   return (
//     <header className="h-20 bg-white dark:bg-slate-900 border-b dark:border-slate-700 flex items-center justify-between px-10 sticky top-0 z-50">
//       <div>
//         <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
//           Dashboard
//         </h1>

//         <p className="text-gray-500 dark:text-slate-400 text-sm">
//           Welcome back to Contract Intelligence AI
//         </p>
//       </div>

//       <div className="flex items-center gap-5">
//         <div className="relative">
//           <Search
//             size={18}
//             className="absolute left-4 top-3 text-gray-400"
//           />

//           <input
//             type="text"
//             placeholder="Search..."
//             className="pl-11 pr-4 py-2 w-72 rounded-xl border bg-gray-50 dark:bg-slate-800 dark:border-slate-700 dark:text-white outline-none focus:ring-2 focus:ring-blue-500"
//           />
//         </div>

//         <button className="w-11 h-11 rounded-xl bg-gray-100 dark:bg-slate-800 dark:text-white hover:bg-gray-200 dark:hover:bg-slate-700 transition flex items-center justify-center">
//           <Bell size={20} />
//         </button>

//         <button
//           onClick={toggleDarkMode}
//           className="w-11 h-11 rounded-xl bg-gray-100 dark:bg-slate-800 dark:text-white hover:bg-gray-200 dark:hover:bg-slate-700 transition flex items-center justify-center"
//         >
//           {darkMode ? <Sun size={20} /> : <Moon size={20} />}
//         </button>

//         <div className="relative" ref={dropdownRef}>
//           <button
//             onClick={() => setOpenProfile(!openProfile)}
//             className="flex items-center gap-3 rounded-2xl px-3 py-2 hover:bg-gray-100 dark:hover:bg-slate-800 transition"
//           >
//             <div className="text-right">
//               <h3 className="font-semibold text-slate-900 dark:text-white">
//                 Mukt Patel
//               </h3>

//               <p className="text-sm text-gray-500 dark:text-slate-400">
//                 Frontend Developer
//               </p>
//             </div>

//             <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
//               M
//             </div>

//             <ChevronDown
//               size={18}
//               className={`text-gray-500 transition ${
//                 openProfile ? "rotate-180" : ""
//               }`}
//             />
//           </button>

//           {openProfile && (
//             <div className="absolute right-0 mt-3 w-64 rounded-2xl bg-white dark:bg-slate-900 dark:text-white border dark:border-slate-700 shadow-2xl p-3 z-50">
//               <div className="px-4 py-3 border-b dark:border-slate-700">
//                 <h3 className="font-bold">Mukt Patel</h3>
//                 <p className="text-sm text-gray-500 dark:text-slate-400">
//                   Frontend Developer
//                 </p>
//               </div>

//              <button
//   onClick={() => {
//     setOpenProfile(false);
//     navigate("/profile");
//   }}
//   className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition"
// >
//   <User size={18} />
//   <span>My Profile</span>
// </button>


// <button
//   onClick={() => {
//     setOpenProfile(false);
//     navigate("/settings");
//   }}
//   className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-gray-100 transition"
// >
//   <Settings size={18} />
//   <span>Settings</span>
// </button>

//               <button
//                 onClick={toggleDarkMode}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 transition"
//               >
//                 {darkMode ? <Sun size={18} /> : <Moon size={18} />}
//                 <span>{darkMode ? "Light Mode" : "Dark Mode"}</span>
//               </button>

//               <button
//                 onClick={handleLogout}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
//               >
//                 <LogOut size={18} />
//                 <span>Logout</span>
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </header>
//   );
// }

// export default Navbar;


// changes no.4 

// import { useEffect, useRef, useState } from "react";
// import {
//   Bell,
//   Search,
//   Moon,
//   User,
//   Settings,
//   LogOut,
//   ChevronDown,
//   FileText,
//   ShieldAlert,
//   MessageSquare,
//   CheckCircle,
// } from "lucide-react";
// import { useNavigate } from "react-router-dom";

// function Navbar() {
//   const [openProfile, setOpenProfile] = useState(false);
//   const [openNotifications, setOpenNotifications] =
//     useState(false);

//   const profileRef = useRef(null);
//   const notificationRef = useRef(null);

//   const navigate = useNavigate();

//   const notifications = [
//     {
//       title: "Contract uploaded successfully",
//       time: "2 hours ago",
//       icon: FileText,
//       color: "bg-blue-100 text-blue-600",
//     },
//     {
//       title: "High risk clause detected",
//       time: "4 hours ago",
//       icon: ShieldAlert,
//       color: "bg-red-100 text-red-600",
//     },
//     {
//       title: "Chatbot answered your query",
//       time: "6 hours ago",
//       icon: MessageSquare,
//       color: "bg-purple-100 text-purple-600",
//     },
//     {
//       title: "Risk analysis completed",
//       time: "Today",
//       icon: CheckCircle,
//       color: "bg-emerald-100 text-emerald-600",
//     },
//   ];

//   useEffect(() => {
//     const handleClickOutside = (e) => {
//       if (
//         profileRef.current &&
//         !profileRef.current.contains(e.target)
//       ) {
//         setOpenProfile(false);
//       }

//       if (
//         notificationRef.current &&
//         !notificationRef.current.contains(e.target)
//       ) {
//         setOpenNotifications(false);
//       }
//     };

//     document.addEventListener("mousedown", handleClickOutside);

//     return () => {
//       document.removeEventListener(
//         "mousedown",
//         handleClickOutside
//       );
//     };
//   }, []);

//   const handleLogout = () => {
//     setOpenProfile(false);
//     navigate("/login");
//   };

//   return (
//     <header className="h-20 bg-white border-b flex items-center justify-between px-10 sticky top-0 z-50">
//       <div>
//         <h1 className="text-2xl font-bold">Dashboard</h1>

//         <p className="text-gray-500 text-sm">
//           Welcome back to Contract Intelligence AI
//         </p>
//       </div>

//       <div className="flex items-center gap-5">
//         <div className="relative">
//           <Search
//             size={18}
//             className="absolute left-4 top-3 text-gray-400"
//           />

//           <input
//             type="text"
//             placeholder="Search..."
//             className="pl-11 pr-4 py-2 w-72 rounded-xl border bg-gray-50 outline-none focus:ring-2 focus:ring-blue-500"
//           />
//         </div>

//         {/* Notifications */}
//         <div className="relative" ref={notificationRef}>
//           <button
//             onClick={() =>
//               setOpenNotifications(!openNotifications)
//             }
//             className="relative w-11 h-11 rounded-xl bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center"
//           >
//             <Bell size={20} />

//             <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[11px] font-bold text-white">
//               4
//             </span>
//           </button>

//           {openNotifications && (
//             <div className="absolute right-0 mt-3 w-96 rounded-2xl bg-white border shadow-2xl p-4 z-50">
//               <div className="mb-4 flex items-center justify-between">
//                 <div>
//                   <h3 className="text-lg font-bold text-slate-900">
//                     Notifications
//                   </h3>

//                   <p className="text-sm text-slate-500">
//                     Latest project updates
//                   </p>
//                 </div>

//                 <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-600">
//                   4 New
//                 </span>
//               </div>

//               <div className="space-y-3">
//                 {notifications.map((item, index) => {
//                   const Icon = item.icon;

//                   return (
//                     <div
//                       key={index}
//                       className="flex items-start gap-3 rounded-xl p-3 hover:bg-slate-50 transition"
//                     >
//                       <div
//                         className={`flex h-10 w-10 items-center justify-center rounded-xl ${item.color}`}
//                       >
//                         <Icon size={18} />
//                       </div>

//                       <div className="flex-1">
//                         <h4 className="font-semibold text-slate-800">
//                           {item.title}
//                         </h4>

//                         <p className="text-sm text-slate-500">
//                           {item.time}
//                         </p>
//                       </div>

//                       <div className="mt-2 h-2 w-2 rounded-full bg-blue-500"></div>
//                     </div>
//                   );
//                 })}
//               </div>

//               <button className="mt-4 w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition">
//                 View All Notifications
//               </button>
//             </div>
//           )}
//         </div>

//         <button className="w-11 h-11 rounded-xl bg-gray-100 hover:bg-gray-200 transition flex items-center justify-center">
//           <Moon size={20} />
//         </button>

//         {/* Profile */}
//         <div className="relative" ref={profileRef}>
//           <button
//             onClick={() => setOpenProfile(!openProfile)}
//             className="flex items-center gap-3 rounded-2xl px-3 py-2 hover:bg-gray-100 transition"
//           >
//             <div className="text-right">
//               <h3 className="font-semibold">Mukt Patel</h3>

//               <p className="text-sm text-gray-500">
//                 Frontend Developer
//               </p>
//             </div>

//             <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
//               M
//             </div>

//             <ChevronDown
//               size={18}
//               className={`text-gray-500 transition ${
//                 openProfile ? "rotate-180" : ""
//               }`}
//             />
//           </button>

//           {openProfile && (
//             <div className="absolute right-0 mt-3 w-64 rounded-2xl bg-white border shadow-2xl p-3 z-50">
//               <div className="px-4 py-3 border-b">
//                 <h3 className="font-bold text-gray-900">
//                   Mukt Patel
//                 </h3>
//                 <p className="text-sm text-gray-500">
//                   Frontend Developer
//                 </p>
//               </div>

//               <button
//                 onClick={() => {
//                   setOpenProfile(false);
//                   navigate("/profile");
//                 }}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition"
//               >
//                 <User size={18} />
//                 <span>My Profile</span>
//               </button>

//               <button
//                 onClick={() => {
//                   setOpenProfile(false);
//                   navigate("/settings");
//                 }}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition"
//               >
//                 <Settings size={18} />
//                 <span>Settings</span>
//               </button>

//               <button className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 transition">
//                 <Moon size={18} />
//                 <span>Dark Mode</span>
//               </button>

//               <button
//                 onClick={handleLogout}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl text-red-600 hover:bg-red-50 transition"
//               >
//                 <LogOut size={18} />
//                 <span>Logout</span>
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </header>
//   );
// }

// export default Navbar;





// import { useEffect, useRef, useState } from "react";
// import {
//   Bell,
//   Search,
//   Moon,
//   Sun,
//   User,
//   Settings,
//   LogOut,
//   ChevronDown,
//   FileText,
//   ShieldAlert,
//   MessageSquare,
//   CheckCircle,
// } from "lucide-react";
// import { useNavigate } from "react-router-dom";
// import { useTheme } from "../../context/ThemeContext";

// function Navbar() {
//   const [openProfile, setOpenProfile] = useState(false);
//   const [openNotifications, setOpenNotifications] = useState(false);

//   const profileRef = useRef(null);
//   const notificationRef = useRef(null);

//   const navigate = useNavigate();
//   const { darkMode, toggleTheme } = useTheme();

//   const notifications = [
//     {
//       title: "Contract uploaded successfully",
//       time: "2 hours ago",
//       icon: FileText,
//       color:
//         "bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300",
//     },
//     {
//       title: "High risk clause detected",
//       time: "4 hours ago",
//       icon: ShieldAlert,
//       color:
//         "bg-red-100 text-red-600 dark:bg-red-900/40 dark:text-red-300",
//     },
//     {
//       title: "Chatbot answered your query",
//       time: "6 hours ago",
//       icon: MessageSquare,
//       color:
//         "bg-purple-100 text-purple-600 dark:bg-purple-900/40 dark:text-purple-300",
//     },
//     {
//       title: "Risk analysis completed",
//       time: "Today",
//       icon: CheckCircle,
//       color:
//         "bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-300",
//     },
//   ];

//   useEffect(() => {
//     const handleClickOutside = (e) => {
//       if (
//         profileRef.current &&
//         !profileRef.current.contains(e.target)
//       ) {
//         setOpenProfile(false);
//       }

//       if (
//         notificationRef.current &&
//         !notificationRef.current.contains(e.target)
//       ) {
//         setOpenNotifications(false);
//       }
//     };

//     document.addEventListener("mousedown", handleClickOutside);

//     return () => {
//       document.removeEventListener(
//         "mousedown",
//         handleClickOutside
//       );
//     };
//   }, []);

//   const handleLogout = () => {
//     setOpenProfile(false);
//     navigate("/login");
//   };

//   return (
//     <header className="h-20 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-10 sticky top-0 z-50 transition-colors">
//       <div>
//         <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
//           Dashboard
//         </h1>

//         <p className="text-gray-500 dark:text-slate-400 text-sm">
//           Welcome back to Contract Intelligence AI
//         </p>
//       </div>

//       <div className="flex items-center gap-5">
//         <div className="relative">
//           <Search
//             size={18}
//             className="absolute left-4 top-3 text-gray-400"
//           />

//           <input
//             type="text"
//             placeholder="Search..."
//             className="pl-11 pr-4 py-2 w-72 rounded-xl border border-slate-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800 text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-blue-500"
//           />
//         </div>

//         <div className="relative" ref={notificationRef}>
//           <button
//             onClick={() =>
//               setOpenNotifications(!openNotifications)
//             }
//             className="relative w-11 h-11 rounded-xl bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white transition flex items-center justify-center"
//           >
//             <Bell size={20} />

//             <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[11px] font-bold text-white">
//               4
//             </span>
//           </button>

//           {openNotifications && (
//             <div className="absolute right-0 mt-3 w-96 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-2xl p-4 z-50">
//               <div className="mb-4 flex items-center justify-between">
//                 <div>
//                   <h3 className="text-lg font-bold text-slate-900 dark:text-white">
//                     Notifications
//                   </h3>

//                   <p className="text-sm text-slate-500 dark:text-slate-400">
//                     Latest project updates
//                   </p>
//                 </div>

//                 <span className="rounded-full bg-blue-50 dark:bg-blue-900/40 px-3 py-1 text-xs font-semibold text-blue-600 dark:text-blue-300">
//                   4 New
//                 </span>
//               </div>

//               <div className="space-y-3">
//                 {notifications.map((item, index) => {
//                   const Icon = item.icon;

//                   return (
//                     <div
//                       key={index}
//                       className="flex items-start gap-3 rounded-xl p-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
//                     >
//                       <div
//                         className={`flex h-10 w-10 items-center justify-center rounded-xl ${item.color}`}
//                       >
//                         <Icon size={18} />
//                       </div>

//                       <div className="flex-1">
//                         <h4 className="font-semibold text-slate-800 dark:text-white">
//                           {item.title}
//                         </h4>

//                         <p className="text-sm text-slate-500 dark:text-slate-400">
//                           {item.time}
//                         </p>
//                       </div>

//                       <div className="mt-2 h-2 w-2 rounded-full bg-blue-500"></div>
//                     </div>
//                   );
//                 })}
//               </div>

//               <button className="mt-4 w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition">
//                 View All Notifications
//               </button>
//             </div>
//           )}
//         </div>

//         <button
//           onClick={toggleTheme}
//           className="w-11 h-11 rounded-xl bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white transition flex items-center justify-center"
//         >
//           {darkMode ? <Sun size={20} /> : <Moon size={20} />}
//         </button>

//         <div className="relative" ref={profileRef}>
//           <button
//             onClick={() => setOpenProfile(!openProfile)}
//             className="flex items-center gap-3 rounded-2xl px-3 py-2 hover:bg-gray-100 dark:hover:bg-slate-800 transition"
//           >
//             <div className="text-right">
//               <h3 className="font-semibold text-slate-900 dark:text-white">
//                 Mukt Patel
//               </h3>

//               <p className="text-sm text-gray-500 dark:text-slate-400">
//                 Frontend Developer
//               </p>
//             </div>

//             <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
//               M
//             </div>

//             <ChevronDown
//               size={18}
//               className={`text-gray-500 transition ${
//                 openProfile ? "rotate-180" : ""
//               }`}
//             />
//           </button>

//           {openProfile && (
//             <div className="absolute right-0 mt-3 w-64 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-2xl p-3 z-50">
//               <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
//                 <h3 className="font-bold text-gray-900 dark:text-white">
//                   Mukt Patel
//                 </h3>

//                 <p className="text-sm text-gray-500 dark:text-slate-400">
//                   Frontend Developer
//                 </p>
//               </div>

//               <button
//                 onClick={() => {
//                   setOpenProfile(false);
//                   navigate("/profile");
//                 }}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-800 dark:text-white transition"
//               >
//                 <User size={18} />
//                 <span>My Profile</span>
//               </button>

//               <button
//                 onClick={() => {
//                   setOpenProfile(false);
//                   navigate("/settings");
//                 }}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-800 dark:text-white transition"
//               >
//                 <Settings size={18} />
//                 <span>Settings</span>
//               </button>

//               <button
//                 onClick={toggleTheme}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-800 dark:text-white transition"
//               >
//                 {darkMode ? <Sun size={18} /> : <Moon size={18} />}
//                 <span>{darkMode ? "Light Mode" : "Dark Mode"}</span>
//               </button>

//               <button
//                 onClick={handleLogout}
//                 className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
//               >
//                 <LogOut size={18} />
//                 <span>Logout</span>
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </header>
//   );
// }

// export default Navbar;




import { useEffect, useRef, useState } from "react";
import {
  Bell,
  Search,
  Moon,
  Sun,
  User,
  Settings,
  LogOut,
  ChevronDown,
  FileText,
  ShieldAlert,
  MessageSquare,
  CheckCircle,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import { useAuth } from "../../context/AuthContext";

function Navbar() {
  const [openProfile, setOpenProfile] = useState(false);
  const [openNotifications, setOpenNotifications] = useState(false);

  const profileRef = useRef(null);
  const notificationRef = useRef(null);

  const navigate = useNavigate();
  const { darkMode, toggleTheme } = useTheme();
  const { currentUser, logout } = useAuth();

  const displayName = currentUser?.name || "User";
  const displayRole = currentUser?.role || "User";
  const avatarLetter = displayName.charAt(0).toUpperCase();

  const notifications = [
    {
      title: "Contract uploaded successfully",
      time: "2 hours ago",
      icon: FileText,
      color:
        "bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300",
    },
    {
      title: "High risk clause detected",
      time: "4 hours ago",
      icon: ShieldAlert,
      color:
        "bg-red-100 text-red-600 dark:bg-red-900/40 dark:text-red-300",
    },
    {
      title: "Chatbot answered your query",
      time: "6 hours ago",
      icon: MessageSquare,
      color:
        "bg-purple-100 text-purple-600 dark:bg-purple-900/40 dark:text-purple-300",
    },
    {
      title: "Risk analysis completed",
      time: "Today",
      icon: CheckCircle,
      color:
        "bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-300",
    },
  ];

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (
        profileRef.current &&
        !profileRef.current.contains(e.target)
      ) {
        setOpenProfile(false);
      }

      if (
        notificationRef.current &&
        !notificationRef.current.contains(e.target)
      ) {
        setOpenNotifications(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    logout();
    setOpenProfile(false);
    navigate("/login");
  };

  return (
    <header className="h-20 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-10 sticky top-0 z-50 transition-colors">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
          Dashboard
        </h1>

        <p className="text-gray-500 dark:text-slate-400 text-sm">
          Welcome back to Contract Intelligence AI
        </p>
      </div>

      <div className="flex items-center gap-5">
        <div className="relative">
          <Search
            size={18}
            className="absolute left-4 top-3 text-gray-400"
          />

          <input
            type="text"
            placeholder="Search..."
            className="pl-11 pr-4 py-2 w-72 rounded-xl border border-slate-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800 text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="relative" ref={notificationRef}>
          <button
            onClick={() => setOpenNotifications(!openNotifications)}
            className="relative w-11 h-11 rounded-xl bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white transition flex items-center justify-center"
          >
            <Bell size={20} />

            <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[11px] font-bold text-white">
              4
            </span>
          </button>

          {openNotifications && (
            <div className="absolute right-0 mt-3 w-96 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-2xl p-4 z-50">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                    Notifications
                  </h3>

                  <p className="text-sm text-slate-500 dark:text-slate-400">
                    Latest project updates
                  </p>
                </div>

                <span className="rounded-full bg-blue-50 dark:bg-blue-900/40 px-3 py-1 text-xs font-semibold text-blue-600 dark:text-blue-300">
                  4 New
                </span>
              </div>

              <div className="space-y-3">
                {notifications.map((item, index) => {
                  const Icon = item.icon;

                  return (
                    <div
                      key={index}
                      className="flex items-start gap-3 rounded-xl p-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
                    >
                      <div
                        className={`flex h-10 w-10 items-center justify-center rounded-xl ${item.color}`}
                      >
                        <Icon size={18} />
                      </div>

                      <div className="flex-1">
                        <h4 className="font-semibold text-slate-800 dark:text-white">
                          {item.title}
                        </h4>

                        <p className="text-sm text-slate-500 dark:text-slate-400">
                          {item.time}
                        </p>
                      </div>

                      <div className="mt-2 h-2 w-2 rounded-full bg-blue-500"></div>
                    </div>
                  );
                })}
              </div>

              <button className="mt-4 w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition">
                View All Notifications
              </button>
            </div>
          )}
        </div>

        <button
          onClick={toggleTheme}
          className="w-11 h-11 rounded-xl bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white transition flex items-center justify-center"
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        <div className="relative" ref={profileRef}>
          <button
            onClick={() => setOpenProfile(!openProfile)}
            className="flex items-center gap-3 rounded-2xl px-3 py-2 hover:bg-gray-100 dark:hover:bg-slate-800 transition"
          >
            <div className="text-right">
              <h3 className="font-semibold text-slate-900 dark:text-white">
                {displayName}
              </h3>

              <p className="text-sm text-gray-500 dark:text-slate-400">
                {displayRole}
              </p>
            </div>

            <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
              {avatarLetter}
            </div>

            <ChevronDown
              size={18}
              className={`text-gray-500 transition ${
                openProfile ? "rotate-180" : ""
              }`}
            />
          </button>

          {openProfile && (
            <div className="absolute right-0 mt-3 w-64 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-2xl p-3 z-50">
              <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
                <h3 className="font-bold text-gray-900 dark:text-white">
                  {displayName}
                </h3>

                <p className="text-sm text-gray-500 dark:text-slate-400">
                  {displayRole}
                </p>
              </div>

              <button
                onClick={() => {
                  setOpenProfile(false);
                  navigate("/profile");
                }}
                className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-800 dark:text-white transition"
              >
                <User size={18} />
                <span>My Profile</span>
              </button>

              <button
                onClick={() => {
                  setOpenProfile(false);
                  navigate("/settings");
                }}
                className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-800 dark:text-white transition"
              >
                <Settings size={18} />
                <span>Settings</span>
              </button>

              <button
                onClick={toggleTheme}
                className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 text-slate-800 dark:text-white transition"
              >
                {darkMode ? <Sun size={18} /> : <Moon size={18} />}
                <span>{darkMode ? "Light Mode" : "Dark Mode"}</span>
              </button>

              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-xl text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
              >
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Navbar;