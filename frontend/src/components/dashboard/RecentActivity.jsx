// function RecentActivity() {
//   const activities = [
//     "Contract uploaded successfully",
//     "Termination clause analyzed",
//     "Chatbot queried for confidentiality",
//     "Risk scoring completed",
//   ];

//   return (
//     <div className="bg-white rounded-xl shadow-md p-6 mt-8">
//       <h2 className="text-2xl font-bold mb-5">
//         Recent Activity
//       </h2>

//       <div className="space-y-4">
//         {activities.map((activity, index) => (
//           <div
//             key={index}
//             className="border-b pb-3 text-gray-700"
//           >
//             • {activity}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// export default RecentActivity;






//recently changed code

// import {
//   UploadCloud,
//   FileSearch,
//   MessageSquare,
//   ShieldCheck,
// } from "lucide-react";

// function RecentActivity() {
//   const activities = [
//     {
//       title: "Contract uploaded successfully",
//       time: "2 hours ago",
//       icon: UploadCloud,
//       color: "bg-blue-100 text-blue-600",
//     },
//     {
//       title: "Termination clause analyzed",
//       time: "4 hours ago",
//       icon: FileSearch,
//       color: "bg-amber-100 text-amber-600",
//     },
//     {
//       title: "Chatbot queried for confidentiality",
//       time: "6 hours ago",
//       icon: MessageSquare,
//       color: "bg-purple-100 text-purple-600",
//     },
//     {
//       title: "Risk scoring completed",
//       time: "Today",
//       icon: ShieldCheck,
//       color: "bg-emerald-100 text-emerald-600",
//     },
//   ];

//   return (
//     <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//       <div className="mb-6 flex items-center justify-between">
//         <div>
//           <h2 className="text-2xl font-bold text-slate-900">
//             Recent Activity
//           </h2>
//           <p className="text-sm text-slate-500">
//             Latest actions across your contract workspace
//           </p>
//         </div>

//         <span className="rounded-full bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-600">
//           Live
//         </span>
//       </div>

//       <div className="space-y-4">
//         {activities.map((activity, index) => {
//           const Icon = activity.icon;

//           return (
//             <div
//               key={index}
//               className="flex items-center justify-between rounded-2xl border border-slate-100 bg-slate-50 p-4 transition hover:bg-white hover:shadow-md"
//             >
//               <div className="flex items-center gap-4">
//                 <div
//                   className={`flex h-12 w-12 items-center justify-center rounded-2xl ${activity.color}`}
//                 >
//                   <Icon size={20} />
//                 </div>

//                 <div>
//                   <h3 className="font-semibold text-slate-800">
//                     {activity.title}
//                   </h3>
//                   <p className="text-sm text-slate-500">
//                     {activity.time}
//                   </p>
//                 </div>
//               </div>

//               <div className="h-2 w-2 rounded-full bg-blue-500"></div>
//             </div>
//           );
//         })}
//       </div>
//     </section>
//   );
// }

// export default RecentActivity;


import {
  UploadCloud,
  FileSearch,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";

function RecentActivity({ contracts = [] }) {
  const generatedActivities = contracts.slice(0, 4).map((contract) => ({
    title: `${contract.filename || "Contract"} uploaded`,
    time: contract.upload_time
      ? new Date(contract.upload_time).toLocaleString()
      : "Recently",
    icon: UploadCloud,
    color:
      "bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300",
  }));

  const fallbackActivities = [
    {
      title: "No recent activity yet",
      time: "Upload a contract to begin",
      icon: FileSearch,
      color:
        "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300",
    },
  ];

  const activities =
    generatedActivities.length > 0 ? generatedActivities : fallbackActivities;

  return (
    <section className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
            Recent Activity
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Latest actions across your contract workspace
          </p>
        </div>

        <span className="rounded-full bg-blue-50 dark:bg-blue-900/40 px-4 py-2 text-sm font-semibold text-blue-600 dark:text-blue-300">
          Live
        </span>
      </div>

      <div className="space-y-4">
        {activities.map((activity, index) => {
          const Icon = activity.icon;

          return (
            <div
              key={index}
              className="flex items-center justify-between rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 p-4 transition hover:bg-white dark:hover:bg-slate-700 hover:shadow-md"
            >
              <div className="flex items-center gap-4">
                <div
                  className={`flex h-12 w-12 items-center justify-center rounded-2xl ${activity.color}`}
                >
                  <Icon size={20} />
                </div>

                <div>
                  <h3 className="font-semibold text-slate-800 dark:text-white">
                    {activity.title}
                  </h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400">
                    {activity.time}
                  </p>
                </div>
              </div>

              <div className="h-2 w-2 rounded-full bg-blue-500"></div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default RecentActivity;