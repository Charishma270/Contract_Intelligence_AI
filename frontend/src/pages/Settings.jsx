// import { useTheme } from "../context/ThemeContext";
// import Layout from "../components/layout/Layout";
// import {
//   Moon,
//   Bell,
//   Shield,
//   Globe,
//   Monitor,
//   Lock,
// } from "lucide-react";

// function Settings() {
//   return (
//     <Layout>
//       {/* Header */}
//       <section className="rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
//         <p className="mb-3 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm">
//           System Preferences
//         </p>

//         <h1 className="text-4xl font-bold">
//           Settings
//         </h1>

//         <p className="mt-3 text-slate-300">
//           Manage your application preferences and account settings.
//         </p>
//       </section>

//       {/* Settings */}
//       <div className="mt-8 grid gap-6">

//         {/* Appearance */}
//         <div className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-blue-100 flex items-center justify-center">
//               <Moon className="text-blue-600" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold">
//                 Appearance
//               </h2>

//               <p className="text-gray-500">
//                 Customize the application theme.
//               </p>
//             </div>
//           </div>

//           <div className="flex items-center justify-between rounded-xl bg-gray-50 p-5">
//             <div>
//               <h3 className="font-semibold">
//                 Dark Mode
//               </h3>

//               <p className="text-sm text-gray-500">
//                 Enable dark appearance.
//               </p>
//             </div>

//             <button className="rounded-xl bg-blue-600 px-5 py-2 text-white hover:bg-blue-700">
//               Enable
//             </button>
//           </div>
//         </div>

//         {/* Notifications */}
//         <div className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-yellow-100 flex items-center justify-center">
//               <Bell className="text-yellow-600" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold">
//                 Notifications
//               </h2>

//               <p className="text-gray-500">
//                 Manage notification preferences.
//               </p>
//             </div>
//           </div>

//           <div className="space-y-4">

//             <label className="flex justify-between rounded-xl bg-gray-50 p-5 cursor-pointer">
//               <span>Email Notifications</span>
//               <input type="checkbox" defaultChecked />
//             </label>

//             <label className="flex justify-between rounded-xl bg-gray-50 p-5 cursor-pointer">
//               <span>Browser Notifications</span>
//               <input type="checkbox" defaultChecked />
//             </label>

//           </div>
//         </div>

//         {/* Security */}
//         <div className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-green-100 flex items-center justify-center">
//               <Shield className="text-green-600" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold">
//                 Security
//               </h2>

//               <p className="text-gray-500">
//                 Protect your account.
//               </p>
//             </div>
//           </div>

//           <div className="space-y-4">

//             <button className="w-full rounded-xl bg-blue-600 py-3 text-white hover:bg-blue-700">
//               <div className="flex items-center justify-center gap-2">
//                 <Lock size={18}/>
//                 Change Password
//               </div>
//             </button>

//             <button className="w-full rounded-xl bg-gray-100 py-3 hover:bg-gray-200">
//               Enable Two-Factor Authentication
//             </button>

//           </div>
//         </div>

//         {/* Language */}
//         <div className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-purple-100 flex items-center justify-center">
//               <Globe className="text-purple-600" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold">
//                 Language
//               </h2>

//               <p className="text-gray-500">
//                 Select your preferred language.
//               </p>
//             </div>
//           </div>

//           <select className="w-full rounded-xl border p-3">
//             <option>English</option>
//             <option>Hindi</option>
//           </select>
//         </div>

//         {/* System */}
//         <div className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-indigo-100 flex items-center justify-center">
//               <Monitor className="text-indigo-600" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold">
//                 System Information
//               </h2>

//               <p className="text-gray-500">
//                 Current application status.
//               </p>
//             </div>
//           </div>

//           <div className="grid md:grid-cols-3 gap-4">

//             <div className="rounded-xl bg-gray-50 p-5">
//               <p className="text-sm text-gray-500">Version</p>
//               <h3 className="text-xl font-bold">v1.0.0</h3>
//             </div>

//             <div className="rounded-xl bg-gray-50 p-5">
//               <p className="text-sm text-gray-500">Backend</p>
//               <h3 className="text-xl font-bold text-green-600">
//                 Connected
//               </h3>
//             </div>

//             <div className="rounded-xl bg-gray-50 p-5">
//               <p className="text-sm text-gray-500">Environment</p>
//               <h3 className="text-xl font-bold">
//                 Development
//               </h3>
//             </div>

//           </div>
//         </div>

//       </div>
//     </Layout>
//   );
// }

// export default Settings;





// import { useTheme } from "../context/ThemeContext";
// import Layout from "../components/layout/Layout";
// import {
//   Moon,
//   Sun,
//   Bell,
//   Shield,
//   Globe,
//   Monitor,
//   Lock,
// } from "lucide-react";

// function Settings() {
//   const { darkMode, toggleTheme } = useTheme();

//   return (
//     <Layout>
//       <section className="rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
//         <p className="mb-3 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm">
//           System Preferences
//         </p>

//         <h1 className="text-4xl font-bold">Settings</h1>

//         <p className="mt-3 text-slate-300">
//           Manage your application preferences and account settings.
//         </p>
//       </section>

//       <div className="mt-8 grid gap-6">
//         <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center">
//               {darkMode ? (
//                 <Sun className="text-blue-300" />
//               ) : (
//                 <Moon className="text-blue-600" />
//               )}
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
//                 Appearance
//               </h2>

//               <p className="text-gray-500 dark:text-slate-400">
//                 Customize the application theme.
//               </p>
//             </div>
//           </div>

//           <div className="flex items-center justify-between rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
//             <div>
//               <h3 className="font-semibold text-slate-900 dark:text-white">
//                 Dark Mode
//               </h3>

//               <p className="text-sm text-gray-500 dark:text-slate-400">
//                 {darkMode
//                   ? "Dark appearance is currently enabled."
//                   : "Enable dark appearance."}
//               </p>
//             </div>

//             <button
//               onClick={toggleTheme}
//               className={`rounded-xl px-5 py-2 font-semibold text-white transition ${
//                 darkMode
//                   ? "bg-emerald-600 hover:bg-emerald-700"
//                   : "bg-blue-600 hover:bg-blue-700"
//               }`}
//             >
//               {darkMode ? "Disable" : "Enable"}
//             </button>
//           </div>
//         </div>

//         <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-yellow-100 dark:bg-yellow-900/40 flex items-center justify-center">
//               <Bell className="text-yellow-600 dark:text-yellow-300" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
//                 Notifications
//               </h2>

//               <p className="text-gray-500 dark:text-slate-400">
//                 Manage notification preferences.
//               </p>
//             </div>
//           </div>

//           <div className="space-y-4">
//             <label className="flex justify-between rounded-xl bg-gray-50 dark:bg-slate-800 p-5 cursor-pointer text-slate-900 dark:text-white transition-colors">
//               <span>Email Notifications</span>
//               <input type="checkbox" defaultChecked />
//             </label>

//             <label className="flex justify-between rounded-xl bg-gray-50 dark:bg-slate-800 p-5 cursor-pointer text-slate-900 dark:text-white transition-colors">
//               <span>Browser Notifications</span>
//               <input type="checkbox" defaultChecked />
//             </label>
//           </div>
//         </div>

//         <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-green-100 dark:bg-green-900/40 flex items-center justify-center">
//               <Shield className="text-green-600 dark:text-green-300" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
//                 Security
//               </h2>

//               <p className="text-gray-500 dark:text-slate-400">
//                 Protect your account.
//               </p>
//             </div>
//           </div>

//           <div className="space-y-4">
//             <button className="w-full rounded-xl bg-blue-600 py-3 text-white hover:bg-blue-700">
//               <div className="flex items-center justify-center gap-2">
//                 <Lock size={18} />
//                 Change Password
//               </div>
//             </button>

//             <button className="w-full rounded-xl bg-gray-100 dark:bg-slate-800 py-3 text-slate-900 dark:text-white hover:bg-gray-200 dark:hover:bg-slate-700 transition-colors">
//               Enable Two-Factor Authentication
//             </button>
//           </div>
//         </div>

//         <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-purple-100 dark:bg-purple-900/40 flex items-center justify-center">
//               <Globe className="text-purple-600 dark:text-purple-300" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
//                 Language
//               </h2>

//               <p className="text-gray-500 dark:text-slate-400">
//                 Select your preferred language.
//               </p>
//             </div>
//           </div>

//           <select className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-slate-900 dark:text-white outline-none">
//             <option>English</option>
//             <option>Hindi</option>
//           </select>
//         </div>

//         <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
//           <div className="flex items-center gap-4 mb-6">
//             <div className="h-12 w-12 rounded-xl bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center">
//               <Monitor className="text-indigo-600 dark:text-indigo-300" />
//             </div>

//             <div>
//               <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
//                 System Information
//               </h2>

//               <p className="text-gray-500 dark:text-slate-400">
//                 Current application status.
//               </p>
//             </div>
//           </div>

//           <div className="grid md:grid-cols-3 gap-4">
//             <div className="rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
//               <p className="text-sm text-gray-500 dark:text-slate-400">
//                 Version
//               </p>
//               <h3 className="text-xl font-bold text-slate-900 dark:text-white">
//                 v1.0.0
//               </h3>
//             </div>

//             <div className="rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
//               <p className="text-sm text-gray-500 dark:text-slate-400">
//                 Backend
//               </p>
//               <h3 className="text-xl font-bold text-green-600 dark:text-green-400">
//                 Connected
//               </h3>
//             </div>

//             <div className="rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
//               <p className="text-sm text-gray-500 dark:text-slate-400">
//                 Environment
//               </p>
//               <h3 className="text-xl font-bold text-slate-900 dark:text-white">
//                 Development
//               </h3>
//             </div>
//           </div>
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Settings;





import { useState } from "react";
import { useTheme } from "../context/ThemeContext";
import Layout from "../components/layout/Layout";
import {
  Moon,
  Sun,
  Bell,
  Shield,
  Globe,
  Monitor,
  Lock,
  X,
  Eye,
  EyeOff,
  CheckCircle,
} from "lucide-react";

function Settings() {
  const { darkMode, toggleTheme } = useTheme();

  const [passwordOpen, setPasswordOpen] = useState(false);
  const [twoFactorOpen, setTwoFactorOpen] = useState(false);
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);

  const [showCurrentPassword, setShowCurrentPassword] =
    useState(false);
  const [showNewPassword, setShowNewPassword] =
    useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  return (
    <Layout>
      <section className="rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
        <p className="mb-3 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm">
          System Preferences
        </p>

        <h1 className="text-4xl font-bold">Settings</h1>

        <p className="mt-3 text-slate-300">
          Manage your application preferences and account settings.
        </p>
      </section>

      <div className="mt-8 grid gap-6">
        <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-12 w-12 rounded-xl bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center">
              {darkMode ? (
                <Sun className="text-blue-300" />
              ) : (
                <Moon className="text-blue-600" />
              )}
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Appearance
              </h2>

              <p className="text-gray-500 dark:text-slate-400">
                Customize the application theme.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
            <div>
              <h3 className="font-semibold text-slate-900 dark:text-white">
                Dark Mode
              </h3>

              <p className="text-sm text-gray-500 dark:text-slate-400">
                {darkMode
                  ? "Dark appearance is currently enabled."
                  : "Enable dark appearance."}
              </p>
            </div>

            <button
              onClick={toggleTheme}
              className={`rounded-xl px-5 py-2 font-semibold text-white transition ${
                darkMode
                  ? "bg-emerald-600 hover:bg-emerald-700"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {darkMode ? "Disable" : "Enable"}
            </button>
          </div>
        </div>

        <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-12 w-12 rounded-xl bg-yellow-100 dark:bg-yellow-900/40 flex items-center justify-center">
              <Bell className="text-yellow-600 dark:text-yellow-300" />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Notifications
              </h2>

              <p className="text-gray-500 dark:text-slate-400">
                Manage notification preferences.
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <label className="flex justify-between rounded-xl bg-gray-50 dark:bg-slate-800 p-5 cursor-pointer text-slate-900 dark:text-white transition-colors">
              <span>Email Notifications</span>
              <input type="checkbox" defaultChecked />
            </label>

            <label className="flex justify-between rounded-xl bg-gray-50 dark:bg-slate-800 p-5 cursor-pointer text-slate-900 dark:text-white transition-colors">
              <span>Browser Notifications</span>
              <input type="checkbox" defaultChecked />
            </label>
          </div>
        </div>

        <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-12 w-12 rounded-xl bg-green-100 dark:bg-green-900/40 flex items-center justify-center">
              <Shield className="text-green-600 dark:text-green-300" />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Security
              </h2>

              <p className="text-gray-500 dark:text-slate-400">
                Protect your account.
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <button
              onClick={() => setPasswordOpen(true)}
              className="w-full rounded-xl bg-blue-600 py-3 text-white hover:bg-blue-700"
            >
              <div className="flex items-center justify-center gap-2">
                <Lock size={18} />
                Change Password
              </div>
            </button>

            <button
              onClick={() => setTwoFactorOpen(true)}
              className={`w-full rounded-xl py-3 font-semibold transition-colors ${
                twoFactorEnabled
                  ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
                  : "bg-gray-100 dark:bg-slate-800 text-slate-900 dark:text-white hover:bg-gray-200 dark:hover:bg-slate-700"
              }`}
            >
              {twoFactorEnabled
                ? "Two-Factor Authentication Enabled"
                : "Enable Two-Factor Authentication"}
            </button>
          </div>
        </div>

        <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-12 w-12 rounded-xl bg-purple-100 dark:bg-purple-900/40 flex items-center justify-center">
              <Globe className="text-purple-600 dark:text-purple-300" />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Language
              </h2>

              <p className="text-gray-500 dark:text-slate-400">
                Select your preferred language.
              </p>
            </div>
          </div>

          <select className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-slate-900 dark:text-white outline-none">
            <option>English</option>
            <option>Hindi</option>
          </select>
        </div>

        <div className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-12 w-12 rounded-xl bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center">
              <Monitor className="text-indigo-600 dark:text-indigo-300" />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                System Information
              </h2>

              <p className="text-gray-500 dark:text-slate-400">
                Current application status.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
              <p className="text-sm text-gray-500 dark:text-slate-400">
                Version
              </p>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                v1.0.0
              </h3>
            </div>

            <div className="rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
              <p className="text-sm text-gray-500 dark:text-slate-400">
                Backend
              </p>
              <h3 className="text-xl font-bold text-green-600 dark:text-green-400">
                Connected
              </h3>
            </div>

            <div className="rounded-xl bg-gray-50 dark:bg-slate-800 p-5 transition-colors">
              <p className="text-sm text-gray-500 dark:text-slate-400">
                Environment
              </p>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                Development
              </h3>
            </div>
          </div>
        </div>
      </div>

      {passwordOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-md rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-2xl border border-slate-100 dark:border-slate-800">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Change Password
              </h2>

              <button
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 p-2 text-slate-700 dark:text-white"
              >
                <X size={20} />
              </button>
            </div>

            <PasswordInput
              placeholder="Current Password"
              show={showCurrentPassword}
              setShow={setShowCurrentPassword}
            />

            <PasswordInput
              placeholder="New Password"
              show={showNewPassword}
              setShow={setShowNewPassword}
            />

            <PasswordInput
              placeholder="Confirm Password"
              show={showConfirmPassword}
              setShow={setShowConfirmPassword}
            />

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 px-5 py-3 font-semibold text-slate-700 dark:text-white"
              >
                Cancel
              </button>

              <button
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
              >
                Update Password
              </button>
            </div>
          </div>
        </div>
      )}

      {twoFactorOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-md rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-2xl border border-slate-100 dark:border-slate-800">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Two-Factor Authentication
              </h2>

              <button
                onClick={() => setTwoFactorOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 p-2 text-slate-700 dark:text-white"
              >
                <X size={20} />
              </button>
            </div>

            <div className="mb-6 rounded-2xl bg-green-50 dark:bg-green-900/30 p-5">
              <div className="flex items-start gap-3">
                <CheckCircle className="text-green-600 dark:text-green-300" />

                <div>
                  <h3 className="font-bold text-slate-900 dark:text-white">
                    Extra account protection
                  </h3>

                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                    Two-Factor Authentication adds an extra verification step
                    when logging in.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setTwoFactorOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 px-5 py-3 font-semibold text-slate-700 dark:text-white"
              >
                Cancel
              </button>

              <button
                onClick={() => {
                  setTwoFactorEnabled(true);
                  setTwoFactorOpen(false);
                }}
                className="rounded-xl bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700"
              >
                Enable
              </button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}

function PasswordInput({ placeholder, show, setShow }) {
  return (
    <div className="relative mb-4">
      <input
        type={show ? "text" : "password"}
        className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 pr-12 text-slate-900 dark:text-white outline-none"
        placeholder={placeholder}
      />

      <button
        type="button"
        onClick={() => setShow(!show)}
        className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 dark:text-slate-400"
      >
        {show ? <EyeOff size={20} /> : <Eye size={20} />}
      </button>
    </div>
  );
}

export default Settings;