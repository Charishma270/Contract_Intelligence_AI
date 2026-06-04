function ContractDetails() {
  const contract = {
    name: "Employment Agreement.pdf",
    status: "Processed",
    risk: "High",
    uploaded: "2 hours ago",
    contractId: "CNT-1001",
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">
      <h2 className="text-2xl font-bold mb-4">
        Contract Details
      </h2>

      <div className="space-y-3">
        <p><strong>Name:</strong> {contract.name}</p>
        <p><strong>ID:</strong> {contract.contractId}</p>
        <p><strong>Status:</strong> {contract.status}</p>
        <p><strong>Risk:</strong> {contract.risk}</p>
        <p><strong>Uploaded:</strong> {contract.uploaded}</p>
      </div>
    </div>
  );
}

export default ContractDetails;