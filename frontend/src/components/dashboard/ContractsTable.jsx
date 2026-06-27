// function ContractsTable() {
//   const contracts = [
//     {
//       name: "Employment Agreement.pdf",
//       status: "Processed",
//       risk: "High",
//       uploaded: "2 hours ago",
//     },
//     {
//       name: "NDA Contract.pdf",
//       status: "Analyzing",
//       risk: "Medium",
//       uploaded: "5 hours ago",
//     },
//     {
//       name: "Vendor Agreement.pdf",
//       status: "Completed",
//       risk: "Low",
//       uploaded: "1 day ago",
//     },
//   ];

//   return (
//     <div className="bg-white rounded-xl shadow-md p-6 mt-8">
//       <div className="flex justify-between items-center mb-6">
//         <h2 className="text-2xl font-bold">
//           Recent Contracts
//         </h2>

//         <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
//           View All
//         </button>
//       </div>

//       <div className="overflow-x-auto">
//         <table className="w-full">
//           <thead>
//             <tr className="border-b text-left">
//               <th className="pb-3">Contract</th>
//               <th className="pb-3">Status</th>
//               <th className="pb-3">Risk</th>
//               <th className="pb-3">Uploaded</th>
//             </tr>
//           </thead>

//           <tbody>
//             {contracts.map((contract, index) => (
//               <tr
//                 key={index}
//                 className="border-b hover:bg-gray-50"
//               >
//                 <td className="py-4 font-medium">
//                   {contract.name}
//                 </td>

//                 <td className="py-4">
//                   <span
//                     className={`px-3 py-1 rounded-full text-sm font-medium ${
//                       contract.status === "Processed"
//                         ? "bg-green-100 text-green-700"
//                         : contract.status === "Analyzing"
//                         ? "bg-yellow-100 text-yellow-700"
//                         : "bg-blue-100 text-blue-700"
//                     }`}
//                   >
//                     {contract.status}
//                   </span>
//                 </td>

//                 <td className="py-4">
//                   <span
//                     className={`font-semibold ${
//                       contract.risk === "High"
//                         ? "text-red-600"
//                         : contract.risk === "Medium"
//                         ? "text-yellow-600"
//                         : "text-green-600"
//                     }`}
//                   >
//                     {contract.risk}
//                   </span>
//                 </td>

//                 <td className="py-4 text-gray-500">
//                   {contract.uploaded}
//                 </td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   );
// }

// export default ContractsTable;


// recent changes

// import { FileText, MoreVertical } from "lucide-react";

// function ContractsTable() {
//   const contracts = [
//     {
//       name: "Employment Agreement.pdf",
//       status: "Processed",
//       risk: "High",
//       uploaded: "2 hours ago",
//     },
//     {
//       name: "NDA Contract.pdf",
//       status: "Analyzing",
//       risk: "Medium",
//       uploaded: "5 hours ago",
//     },
//     {
//       name: "Vendor Agreement.pdf",
//       status: "Completed",
//       risk: "Low",
//       uploaded: "1 day ago",
//     },
//   ];

//   const statusStyle = {
//     Processed: "bg-emerald-100 text-emerald-700",
//     Analyzing: "bg-amber-100 text-amber-700",
//     Completed: "bg-blue-100 text-blue-700",
//   };

//   const riskStyle = {
//     High: "bg-red-100 text-red-700",
//     Medium: "bg-orange-100 text-orange-700",
//     Low: "bg-green-100 text-green-700",
//   };

//   return (
//     <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//       <div className="mb-6 flex items-center justify-between">
//         <div>
//           <h2 className="text-2xl font-bold text-slate-900">
//             Recent Contracts
//           </h2>
//           <p className="text-sm text-slate-500">
//             Recently uploaded and analyzed contracts
//           </p>
//         </div>

//         <button className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700">
//           View All
//         </button>
//       </div>

//       <div className="overflow-hidden rounded-2xl border border-slate-100">
//         <table className="w-full">
//           <thead className="bg-slate-50">
//             <tr className="text-left text-sm text-slate-500">
//               <th className="px-5 py-4">Contract</th>
//               <th className="px-5 py-4">Status</th>
//               <th className="px-5 py-4">Risk</th>
//               <th className="px-5 py-4">Uploaded</th>
//               <th className="px-5 py-4 text-right">Action</th>
//             </tr>
//           </thead>

//           <tbody className="divide-y divide-slate-100">
//             {contracts.map((contract, index) => (
//               <tr
//                 key={index}
//                 className="transition hover:bg-slate-50"
//               >
//                 <td className="px-5 py-5">
//                   <div className="flex items-center gap-3">
//                     <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
//                       <FileText size={20} />
//                     </div>

//                     <span className="font-semibold text-slate-800">
//                       {contract.name}
//                     </span>
//                   </div>
//                 </td>

//                 <td className="px-5 py-5">
//                   <span
//                     className={`rounded-full px-3 py-1 text-xs font-semibold ${statusStyle[contract.status]}`}
//                   >
//                     {contract.status}
//                   </span>
//                 </td>

//                 <td className="px-5 py-5">
//                   <span
//                     className={`rounded-full px-3 py-1 text-xs font-semibold ${riskStyle[contract.risk]}`}
//                   >
//                     {contract.risk}
//                   </span>
//                 </td>

//                 <td className="px-5 py-5 text-slate-500">
//                   {contract.uploaded}
//                 </td>

//                 <td className="px-5 py-5 text-right">
//                   <button className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700">
//                     <MoreVertical size={18} />
//                   </button>
//                 </td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </section>
//   );
// }

// export default ContractsTable;



import { Link } from "react-router-dom";
import { FileText, MoreVertical } from "lucide-react";

function ContractsTable({ contracts = [], loading = false }) {
  const normalizedContracts = contracts.slice(0, 5).map((item) => ({
    name: item.filename || item.name || "Untitled Contract",
    status: item.status || "uploaded",
    risk: item.risk || item.risk_level || "N/A",
    uploaded: item.upload_time
      ? new Date(item.upload_time).toLocaleString()
      : item.uploaded || "N/A",
  }));

  const statusStyle = {
    uploaded: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
    processing: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
    analyzing: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
    completed: "bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300",
    failed: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
  };

  const riskStyle = {
    High: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
    Medium: "bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300",
    Low: "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300",
    "N/A": "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  };

  return (
    <section className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
            Recent Contracts
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Recently uploaded and analyzed contracts
          </p>
        </div>

        <Link
          to="/viewer"
          className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
        >
          View All
        </Link>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-100 dark:border-slate-800">
        {loading ? (
          <div className="p-8 text-center text-slate-500 dark:text-slate-400">
            Loading contracts...
          </div>
        ) : normalizedContracts.length === 0 ? (
          <div className="p-8 text-center text-slate-500 dark:text-slate-400">
            No contracts uploaded yet.
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-slate-50 dark:bg-slate-800">
              <tr className="text-left text-sm text-slate-500 dark:text-slate-400">
                <th className="px-5 py-4">Contract</th>
                <th className="px-5 py-4">Status</th>
                <th className="px-5 py-4">Risk</th>
                <th className="px-5 py-4">Uploaded</th>
                <th className="px-5 py-4 text-right">Action</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {normalizedContracts.map((contract, index) => (
                <tr
                  key={index}
                  className="transition hover:bg-slate-50 dark:hover:bg-slate-800"
                >
                  <td className="px-5 py-5">
                    <div className="flex items-center gap-3">
                      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-300">
                        <FileText size={20} />
                      </div>

                      <span className="font-semibold text-slate-800 dark:text-white">
                        {contract.name}
                      </span>
                    </div>
                  </td>

                  <td className="px-5 py-5">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        statusStyle[contract.status] ||
                        statusStyle.uploaded
                      }`}
                    >
                      {contract.status}
                    </span>
                  </td>

                  <td className="px-5 py-5">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        riskStyle[contract.risk] || riskStyle["N/A"]
                      }`}
                    >
                      {contract.risk}
                    </span>
                  </td>

                  <td className="px-5 py-5 text-slate-500 dark:text-slate-400">
                    {contract.uploaded}
                  </td>

                  <td className="px-5 py-5 text-right">
                    <button className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-white">
                      <MoreVertical size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}

export default ContractsTable;