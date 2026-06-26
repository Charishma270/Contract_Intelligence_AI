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
function RiskChart() {
  const data = [
    {
      risk: "High",
      count: 5,
      color: "bg-red-500",
      bg: "bg-red-50",
      text: "text-red-600",
    },
    {
      risk: "Medium",
      count: 14,
      color: "bg-amber-500",
      bg: "bg-amber-50",
      text: "text-amber-600",
    },
    {
      risk: "Low",
      count: 22,
      color: "bg-emerald-500",
      bg: "bg-emerald-50",
      text: "text-emerald-600",
    },
  ];

  const maxCount = Math.max(...data.map((item) => item.count));

  return (
    <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
      <div className="mb-7 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">
            Risk Distribution
          </h2>
          <p className="text-sm text-slate-500">
            Clause severity distribution across uploaded contracts
          </p>
        </div>

        <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-600">
          Total 41
        </span>
      </div>

      <div className="space-y-6">
        {data.map((item, index) => (
          <div
            key={index}
            className={`rounded-2xl ${item.bg} p-5`}
          >
            <div className="mb-3 flex items-center justify-between">
              <span className={`font-bold ${item.text}`}>
                {item.risk} Risk
              </span>

              <span className="font-bold text-slate-900">
                {item.count}
              </span>
            </div>

            <div className="h-4 w-full rounded-full bg-white">
              <div
                className={`${item.color} h-4 rounded-full transition-all duration-700`}
                style={{
                  width: `${(item.count / maxCount) * 100}%`,
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default RiskChart;