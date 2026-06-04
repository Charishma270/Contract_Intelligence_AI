// import Layout from "../components/layout/Layout";

// function Dashboard() {
//   return (
//     <Layout>
//       <h2 className="text-2xl font-bold mb-4">Dashboard Overview</h2>

//       <div className="grid grid-cols-3 gap-4">
//         <div className="bg-white p-4 shadow rounded">
//           Total Contracts
//         </div>

//         <div className="bg-white p-4 shadow rounded">
//           Risk Score
//         </div>

//         <div className="bg-white p-4 shadow rounded">
//           Entities Extracted
//         </div>
//       </div>
//     </Layout>
//   );
// }

// export default Dashboard;

// week 4 mondayyyyyy


import Layout from "../components/layout/Layout";
import StatsCard from "../components/dashboard/StatsCard";
import RecentActivity from "../components/dashboard/RecentActivity";
import ContractsTable from "../components/dashboard/ContractsTable";
import RiskChart from "../components/dashboard/RiskChart";
import ContractDetails from "../components/dashboard/ContractDetails";

function Dashboard() {
  const stats = [
    {
      title: "Total Contracts",
      value: 12,
      color: "#2563eb",
    },
    {
      title: "High Risk Clauses",
      value: 5,
      color: "#dc2626",
    },
    {
      title: "Medium Risk Clauses",
      value: 14,
      color: "#ca8a04",
    },
    {
      title: "Low Risk Clauses",
      value: 22,
      color: "#16a34a",
    },
  ];

  return (
    <Layout>
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          AI Contract Dashboard
        </h1>

        <p className="text-gray-600">
          Monitor contracts, risks, and AI analysis.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {stats.map((item, index) => (
          <StatsCard
            key={index}
            title={item.title}
            value={item.value}
            color={item.color}
          />
        ))}
      </div>
      <RecentActivity />
      <ContractsTable />
      <RiskChart />
      <ContractDetails />
    </Layout>
  );
}

export default Dashboard;