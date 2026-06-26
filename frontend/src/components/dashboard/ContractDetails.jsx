// function ContractDetails() {
//   const contract = {
//     name: "Employment Agreement.pdf",
//     status: "Processed",
//     risk: "High",
//     uploaded: "2 hours ago",
//     contractId: "CNT-1001",
//   };

//   return (
//     <div className="bg-white rounded-xl shadow-md p-6 mt-8">
//       <h2 className="text-2xl font-bold mb-4">
//         Contract Details
//       </h2>

//       <div className="space-y-3">
//         <p><strong>Name:</strong> {contract.name}</p>
//         <p><strong>ID:</strong> {contract.contractId}</p>
//         <p><strong>Status:</strong> {contract.status}</p>
//         <p><strong>Risk:</strong> {contract.risk}</p>
//         <p><strong>Uploaded:</strong> {contract.uploaded}</p>
//       </div>
//     </div>
//   );
// }

// export default ContractDetails;


//recent changes

import {
  FileText,
  Hash,
  Clock,
  ShieldAlert,
  CheckCircle,
} from "lucide-react";

function ContractDetails() {
  const contract = {
    name: "Employment Agreement.pdf",
    status: "Processed",
    risk: "High",
    uploaded: "2 hours ago",
    contractId: "CNT-1001",
  };

  const details = [
    {
      label: "Contract Name",
      value: contract.name,
      icon: FileText,
      color: "bg-blue-100 text-blue-600",
    },
    {
      label: "Contract ID",
      value: contract.contractId,
      icon: Hash,
      color: "bg-slate-100 text-slate-600",
    },
    {
      label: "Status",
      value: contract.status,
      icon: CheckCircle,
      color: "bg-emerald-100 text-emerald-600",
    },
    {
      label: "Risk Level",
      value: contract.risk,
      icon: ShieldAlert,
      color: "bg-red-100 text-red-600",
    },
    {
      label: "Uploaded",
      value: contract.uploaded,
      icon: Clock,
      color: "bg-purple-100 text-purple-600",
    },
  ];

  return (
    <section className="rounded-3xl bg-white p-7 shadow-sm border border-slate-100">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900">
          Contract Details
        </h2>
        <p className="text-sm text-slate-500">
          Selected contract overview and processing status
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {details.map((item, index) => {
          const Icon = item.icon;

          return (
            <div
              key={index}
              className="rounded-2xl border border-slate-100 bg-slate-50 p-5 transition hover:bg-white hover:shadow-md"
            >
              <div className="mb-4 flex items-center gap-3">
                <div
                  className={`flex h-11 w-11 items-center justify-center rounded-xl ${item.color}`}
                >
                  <Icon size={20} />
                </div>

                <p className="text-sm font-semibold text-slate-500">
                  {item.label}
                </p>
              </div>

              <h3 className="font-bold text-slate-900">
                {item.value}
              </h3>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default ContractDetails;