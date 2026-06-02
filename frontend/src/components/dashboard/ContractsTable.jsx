function ContractsTable() {
  const contracts = [
    {
      name: "Employment Agreement.pdf",
      status: "Processed",
      risk: "High",
      uploaded: "2 hours ago",
    },
    {
      name: "NDA Contract.pdf",
      status: "Analyzing",
      risk: "Medium",
      uploaded: "5 hours ago",
    },
    {
      name: "Vendor Agreement.pdf",
      status: "Completed",
      risk: "Low",
      uploaded: "1 day ago",
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">
          Recent Contracts
        </h2>

        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
          View All
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b text-left">
              <th className="pb-3">Contract</th>
              <th className="pb-3">Status</th>
              <th className="pb-3">Risk</th>
              <th className="pb-3">Uploaded</th>
            </tr>
          </thead>

          <tbody>
            {contracts.map((contract, index) => (
              <tr
                key={index}
                className="border-b hover:bg-gray-50"
              >
                <td className="py-4 font-medium">
                  {contract.name}
                </td>

                <td className="py-4">
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      contract.status === "Processed"
                        ? "bg-green-100 text-green-700"
                        : contract.status === "Analyzing"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-blue-100 text-blue-700"
                    }`}
                  >
                    {contract.status}
                  </span>
                </td>

                <td className="py-4">
                  <span
                    className={`font-semibold ${
                      contract.risk === "High"
                        ? "text-red-600"
                        : contract.risk === "Medium"
                        ? "text-yellow-600"
                        : "text-green-600"
                    }`}
                  >
                    {contract.risk}
                  </span>
                </td>

                <td className="py-4 text-gray-500">
                  {contract.uploaded}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ContractsTable;