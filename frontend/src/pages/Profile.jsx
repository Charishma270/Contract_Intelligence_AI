// import Layout from "../components/layout/Layout";
// import {
//   User,
//   Mail,
//   Briefcase,
//   Phone,
//   Building2,
//   Calendar,
//   Clock,
//   ShieldCheck,
// } from "lucide-react";

// function Profile() {
//   const user = {
//     name: "Mukt Patel",
//     email: "muktpatel@example.com",
//     role: "Frontend Developer",
//     phone: "+91 98765 43210",
//     organization: "Zaalima Development Ltd.",
//     userId: "USR-1001",
//     joinedDate: "June 2026",
//     lastLogin: "Today",
//   };

//   const info = [
//     {
//       label: "Full Name",
//       value: user.name,
//       icon: User,
//       color: "bg-blue-100 text-blue-600",
//     },
//     {
//       label: "Email Address",
//       value: user.email,
//       icon: Mail,
//       color: "bg-purple-100 text-purple-600",
//     },
//     {
//       label: "Role",
//       value: user.role,
//       icon: Briefcase,
//       color: "bg-emerald-100 text-emerald-600",
//     },
//     {
//       label: "Phone Number",
//       value: user.phone,
//       icon: Phone,
//       color: "bg-orange-100 text-orange-600",
//     },
//     {
//       label: "Organization",
//       value: user.organization,
//       icon: Building2,
//       color: "bg-indigo-100 text-indigo-600",
//     },
//     {
//       label: "User ID",
//       value: user.userId,
//       icon: ShieldCheck,
//       color: "bg-red-100 text-red-600",
//     },
//     {
//       label: "Joined Date",
//       value: user.joinedDate,
//       icon: Calendar,
//       color: "bg-cyan-100 text-cyan-600",
//     },
//     {
//       label: "Last Login",
//       value: user.lastLogin,
//       icon: Clock,
//       color: "bg-slate-100 text-slate-600",
//     },
//   ];

//   return (
//     <Layout>
//       <section className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
//         <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
//           <div className="flex items-center gap-5">
//             <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-blue-600 text-4xl font-bold shadow-lg">
//               M
//             </div>

//             <div>
//               <p className="mb-2 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-blue-100">
//                 User Profile
//               </p>

//               <h1 className="text-4xl font-bold">
//                 {user.name}
//               </h1>

//               <p className="mt-2 text-slate-300">
//                 {user.role} • {user.organization}
//               </p>
//             </div>
//           </div>

//           <button className="rounded-xl bg-white px-5 py-3 font-semibold text-slate-900 hover:bg-slate-100">
//             Edit Profile
//           </button>
//         </div>
//       </section>

//       <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//         <div className="mb-6">
//           <h2 className="text-2xl font-bold text-slate-900">
//             Account Information
//           </h2>
//           <p className="text-sm text-slate-500">
//             Personal details and account activity
//           </p>
//         </div>

//         <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
//           {info.map((item, index) => {
//             const Icon = item.icon;

//             return (
//               <div
//                 key={index}
//                 className="rounded-2xl border border-slate-100 bg-slate-50 p-5 transition hover:bg-white hover:shadow-md"
//               >
//                 <div className="mb-4 flex items-center gap-3">
//                   <div
//                     className={`flex h-11 w-11 items-center justify-center rounded-xl ${item.color}`}
//                   >
//                     <Icon size={20} />
//                   </div>

//                   <p className="text-sm font-semibold text-slate-500">
//                     {item.label}
//                   </p>
//                 </div>

//                 <h3 className="font-bold text-slate-900">
//                   {item.value}
//                 </h3>
//               </div>
//             );
//           })}
//         </div>
//       </section>

//       <section className="mt-8 rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//         <div className="mb-6">
//           <h2 className="text-2xl font-bold text-slate-900">
//             Security
//           </h2>
//           <p className="text-sm text-slate-500">
//             Manage account security options
//           </p>
//         </div>

//         <div className="flex flex-col gap-4 md:flex-row">
//           <button className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700">
//             Change Password
//           </button>

//           <button className="rounded-xl bg-slate-100 px-6 py-3 font-semibold text-slate-700 hover:bg-slate-200">
//             Enable Two-Factor Auth
//           </button>
//         </div>
//       </section>
//     </Layout>
//   );
// }

// export default Profile;




import { useState } from "react";
import Layout from "../components/layout/Layout";
import { useAuth } from "../context/AuthContext";
import {
  User,
  Mail,
  Briefcase,
  Phone,
  Building2,
  Calendar,
  Clock,
  ShieldCheck,
  X,
  Eye,
  EyeOff,
} from "lucide-react";

function Profile() {
  const [editOpen, setEditOpen] = useState(false);
  const [passwordOpen, setPasswordOpen] = useState(false);
  const [twoFactor, setTwoFactor] = useState(false);

  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const { currentUser, updateProfile, changePassword } = useAuth();

  const [editData, setEditData] = useState({
  name: currentUser?.name || "",
  email: currentUser?.email || "",
  phone: currentUser?.phone || "",
  organization: currentUser?.organization || "",
});

const [passwordData, setPasswordData] = useState({
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const [message, setMessage] = useState("");

  // const user = {
  //   name: "Mukt Patel",
  //   email: "muktpatel@example.com",
  //   role: "Frontend Developer",
  //   phone: "+91 98765 43210",
  //   organization: "Zaalima Development Ltd.",
  //   userId: "USR-1001",
  //   joinedDate: "June 2026",
  //   lastLogin: "Today",
  // };


  const user = {
  name: currentUser?.name || "User",
  email: currentUser?.email || "user@example.com",
  role: currentUser?.role || "User",
  phone: currentUser?.phone || "N/A",
  organization: currentUser?.organization || "N/A",
  userId: currentUser?.id ? `USR-${currentUser.id}` : "USR-1001",
  joinedDate: currentUser?.joinedDate || "N/A",
  lastLogin: currentUser?.lastLogin || "Today",
};

  const info = [
    {
      label: "Full Name",
      value: user.name,
      icon: User,
      color:
        "bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300",
    },
    {
      label: "Email Address",
      value: user.email,
      icon: Mail,
      color:
        "bg-purple-100 text-purple-600 dark:bg-purple-900/40 dark:text-purple-300",
    },
    {
      label: "Role",
      value: user.role,
      icon: Briefcase,
      color:
        "bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-300",
    },
    {
      label: "Phone Number",
      value: user.phone,
      icon: Phone,
      color:
        "bg-orange-100 text-orange-600 dark:bg-orange-900/40 dark:text-orange-300",
    },
    {
      label: "Organization",
      value: user.organization,
      icon: Building2,
      color:
        "bg-indigo-100 text-indigo-600 dark:bg-indigo-900/40 dark:text-indigo-300",
    },
    {
      label: "User ID",
      value: user.userId,
      icon: ShieldCheck,
      color:
        "bg-red-100 text-red-600 dark:bg-red-900/40 dark:text-red-300",
    },
    {
      label: "Joined Date",
      value: user.joinedDate,
      icon: Calendar,
      color:
        "bg-cyan-100 text-cyan-600 dark:bg-cyan-900/40 dark:text-cyan-300",
    },
    {
      label: "Last Login",
      value: user.lastLogin,
      icon: Clock,
      color:
        "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300",
    },
  ];

  return (
    <Layout>
      <section className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-5">
            <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-blue-600 text-4xl font-bold shadow-lg">
                {user.name.charAt(0).toUpperCase()}
            </div>

            <div>
              <p className="mb-2 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-blue-100">
                User Profile
              </p>

              <h1 className="text-4xl font-bold">
                {user.name}
              </h1>

              <p className="mt-2 text-slate-300">
                {user.role} • {user.organization}
              </p>
            </div>
          </div>

          <button
            onClick={() => setEditOpen(true)}
            className="rounded-xl bg-white px-5 py-3 font-semibold text-slate-900 hover:bg-slate-100"
          >
            Edit Profile
          </button>
        </div>
      </section>

      <section className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
            Account Information
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Personal details and account activity
          </p>
        </div>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {info.map((item, index) => {
            const Icon = item.icon;

            return (
              <div
                key={index}
                className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 p-5 transition hover:bg-white dark:hover:bg-slate-700 hover:shadow-md"
              >
                <div className="mb-4 flex items-center gap-3">
                  <div
                    className={`flex h-11 w-11 items-center justify-center rounded-xl ${item.color}`}
                  >
                    <Icon size={20} />
                  </div>

                  <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">
                    {item.label}
                  </p>
                </div>

                <h3 className="font-bold text-slate-900 dark:text-white">
                  {item.value}
                </h3>
              </div>
            );
          })}
        </div>
      </section>

      <section className="mt-8 rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800 transition-colors">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
            Security
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Manage account security options
          </p>
        </div>

        <div className="flex flex-col gap-4 md:flex-row">
          <button
            onClick={() => setPasswordOpen(true)}
            className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
          >
            Change Password
          </button>

          <button
            onClick={() => setTwoFactor(!twoFactor)}
            className={`rounded-xl px-6 py-3 font-semibold transition ${
              twoFactor
                ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700"
            }`}
          >
            {twoFactor
              ? "Two-Factor Enabled"
              : "Enable Two-Factor Auth"}
          </button>
        </div>
      </section>

      {editOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-lg rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-2xl border border-slate-100 dark:border-slate-800">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Edit Profile
              </h2>

              <button
                onClick={() => setEditOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 p-2 text-slate-700 dark:text-white"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-4">
              <input
                className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-slate-900 dark:text-white outline-none"
                placeholder="Full Name"
                value={editData.name}
  onChange={(e) =>
    setEditData({ ...editData, name: e.target.value })
  }
/>
              <input
                className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-slate-900 dark:text-white outline-none"
                placeholder="Email"
                value={editData.email}
                onChange={(e) =>
                  setEditData({ ...editData, email: e.target.value })
                }
              />
              <input
                className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-slate-900 dark:text-white outline-none"
                placeholder="Phone"
                value={editData.phone}
                onChange={(e) =>
                  setEditData({ ...editData, phone: e.target.value })
                }
              />
              <input
                className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-slate-900 dark:text-white outline-none"
                placeholder="Organization"
                value={editData.organization}
                onChange={(e) =>
                  setEditData({ ...editData, organization: e.target.value })
                }
              />
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setEditOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 px-5 py-3 font-semibold text-slate-700 dark:text-white"
              >
                Cancel
              </button>

              <button
  onClick={ async () => {
    const result = await updateProfile(editData);
    setMessage(result.message);

    if (result.success) {
      setEditOpen(false);
    }
  }}
  className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
>
  Save Changes
</button>
            </div>
          </div>
        </div>
      )}

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
  value={passwordData.currentPassword}
  onChange={(e) =>
    setPasswordData({
      ...passwordData,
      currentPassword: e.target.value,
    })
  }
/>

            <PasswordInput
              placeholder="New Password"
              show={showNewPassword}
              setShow={setShowNewPassword}
              value={passwordData.newPassword}
              onChange={(e) =>
                setPasswordData({
                  ...passwordData,
                  newPassword: e.target.value,
                })
              }
            />

            <PasswordInput
              placeholder="Confirm Password"
              show={showConfirmPassword}
              setShow={setShowConfirmPassword}
              value={passwordData.confirmPassword}
              onChange={(e) =>
                setPasswordData({
                  ...passwordData,
                  confirmPassword: e.target.value,
                })
              }
            />

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl bg-slate-100 dark:bg-slate-800 px-5 py-3 font-semibold text-slate-700 dark:text-white"
              >
                Cancel
              </button>

              <button
  onClick={ async () => {
    const result = await changePassword(passwordData);
    setMessage(result.message);

    if (result.success) {
      setPasswordOpen(false);
      setPasswordData({
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      });
    }
  }}
  className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
>
  Update Password
</button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}
function PasswordInput({
  placeholder,
  show,
  setShow,
  value,
  onChange,
}) {
  return (
    <div className="relative mb-4">
      <input
        type={show ? "text" : "password"}
        value={value}
        onChange={onChange}
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
export default Profile;