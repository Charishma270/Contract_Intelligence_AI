// function RiskChart() {
//   const data = [
//     { risk: "High", count: 5, color: "bg-red-500" },
//     { risk: "Medium", count: 14, color: "bg-yellow-500" },
//     { risk: "Low", count: 22, color: "bg-green-500" },
//   ];

//   const maxCount = Math.max(...data.map((item) => item.count));

//   return (
//     <div className="bg-white rounded-xl shadow-md p-6 mt-8">
//       <h2 className="text-2xl font-bold mb-5">Risk Distribution</h2>

//       <div className="space-y-5">
//         {data.map((item, index) => (
//           <div key={index}>
//             <div className="flex justify-between mb-2">
//               <span className="font-medium">{item.risk}</span>
//               <span className="font-bold">{item.count}</span>
//             </div>

//             <div className="w-full bg-gray-200 rounded-full h-4">
//               <div
//                 className={`${item.color} h-4 rounded-full`}
//                 style={{
//                   width: `${(item.count / maxCount) * 100}%`,
//                 }}
//               ></div>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// export default RiskChart;




// recent changes
// function RiskChart() {
//   const data = [
//     {
//       risk: "High",
//       count: 5,
//       color: "bg-red-500",
//       bg: "bg-red-50",
//       text: "text-red-600",
//     },
//     {
//       risk: "Medium",
//       count: 14,
//       color: "bg-amber-500",
//       bg: "bg-amber-50",
//       text: "text-amber-600",
//     },
//     {
//       risk: "Low",
//       count: 22,
//       color: "bg-emerald-500",
//       bg: "bg-emerald-50",
//       text: "text-emerald-600",
//     },
//   ];

//   const maxCount = Math.max(...data.map((item) => item.count));

//   return (
//     <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
//       <div className="mb-7 flex items-center justify-between">
//         <div>
//           <h2 className="text-2xl font-bold text-slate-900">
//             Risk Distribution
//           </h2>
//           <p className="text-sm text-slate-500">
//             Clause severity distribution across uploaded contracts
//           </p>
//         </div>

//         <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-600">
//           Total 41
//         </span>
//       </div>

//       <div className="space-y-6">
//         {data.map((item, index) => (
//           <div
//             key={index}
//             className={`rounded-2xl ${item.bg} p-5`}
//           >
//             <div className="mb-3 flex items-center justify-between">
//               <span className={`font-bold ${item.text}`}>
//                 {item.risk} Risk
//               </span>

//               <span className="font-bold text-slate-900">
//                 {item.count}
//               </span>
//             </div>

//             <div className="h-4 w-full rounded-full bg-white">
//               <div
//                 className={`${item.color} h-4 rounded-full transition-all duration-700`}
//                 style={{
//                   width: `${(item.count / maxCount) * 100}%`,
//                 }}
//               ></div>
//             </div>
//           </div>
//         ))}
//       </div>
//     </section>
//   );
// }

// export default RiskChart;


function RiskChart({ contracts = [] }) {
  const getRisk = (contract) => {
    return (
      contract.risk ||
      contract.risk_level ||
      contract.overall_risk ||
      "N/A"
    );
  };

  const highCount = contracts.filter(
    (contract) => getRisk(contract).toLowerCase() === "high"
  ).length;

  const mediumCount = contracts.filter(
    (contract) => getRisk(contract).toLowerCase() === "medium"
  ).length;

  const lowCount = contracts.filter(
    (contract) => getRisk(contract).toLowerCase() === "low"
  ).length;

  const unknownCount = contracts.filter((contract) => {
    const risk = getRisk(contract).toLowerCase();
    return !["high", "medium", "low"].includes(risk);
  }).length;

  const data = [
    {
      risk: "High",
      count: highCount,
      color: "bg-red-500",
      bg: "bg-red-50 dark:bg-red-900/30",
      text: "text-red-600 dark:text-red-300",
    },
    {
      risk: "Medium",
      count: mediumCount,
      color: "bg-amber-500",
      bg: "bg-amber-50 dark:bg-amber-900/30",
      text: "text-amber-600 dark:text-amber-300",
    },
    {
      risk: "Low",
      count: lowCount,
      color: "bg-emerald-500",
      bg: "bg-emerald-50 dark:bg-emerald-900/30",
      text: "text-emerald-600 dark:text-emerald-300",
    },
    {
      risk: "Unknown",
      count: unknownCount,
      color: "bg-slate-500",
      bg: "bg-slate-50 dark:bg-slate-800",
      text: "text-slate-600 dark:text-slate-300",
    },
  ];

  const total = data.reduce((sum, item) => sum + item.count, 0);
  const maxCount = Math.max(...data.map((item) => item.count), 1);

  return (
    <section className="rounded-3xl bg-white dark:bg-slate-900 p-7 shadow-sm border border-slate-100 dark:border-slate-800">
      <div className="mb-7 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
            Risk Distribution
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Risk severity distribution across uploaded contracts
          </p>
        </div>

        <span className="rounded-full bg-slate-100 dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-600 dark:text-slate-300">
          Total {total}
        </span>
      </div>

      {contracts.length === 0 ? (
        <div className="rounded-2xl bg-slate-50 dark:bg-slate-800 p-6 text-center text-slate-500 dark:text-slate-400">
          No risk data available yet.
        </div>
      ) : (
        <div className="space-y-6">
          {data.map((item, index) => (
            <div key={index} className={`rounded-2xl ${item.bg} p-5`}>
              <div className="mb-3 flex items-center justify-between">
                <span className={`font-bold ${item.text}`}>
                  {item.risk} Risk
                </span>

                <span className="font-bold text-slate-900 dark:text-white">
                  {item.count}
                </span>
              </div>

              <div className="h-4 w-full rounded-full bg-white dark:bg-slate-700">
                <div
                  className={`${item.color} h-4 rounded-full transition-all duration-700`}
                  style={{
                    width:
                      item.count === 0
                        ? "0%"
                        : `${(item.count / maxCount) * 100}%`,
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default RiskChart;