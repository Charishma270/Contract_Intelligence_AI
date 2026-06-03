function RiskChart() {
  const data = [
    { risk: "High", count: 5, color: "bg-red-500" },
    { risk: "Medium", count: 14, color: "bg-yellow-500" },
    { risk: "Low", count: 22, color: "bg-green-500" },
  ];

  const maxCount = Math.max(...data.map((item) => item.count));

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">
      <h2 className="text-2xl font-bold mb-5">Risk Distribution</h2>

      <div className="space-y-5">
        {data.map((item, index) => (
          <div key={index}>
            <div className="flex justify-between mb-2">
              <span className="font-medium">{item.risk}</span>
              <span className="font-bold">{item.count}</span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className={`${item.color} h-4 rounded-full`}
                style={{
                  width: `${(item.count / maxCount) * 100}%`,
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RiskChart;