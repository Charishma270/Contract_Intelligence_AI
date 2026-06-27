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


// import Layout from "../components/layout/Layout";
// import StatsCard from "../components/dashboard/StatsCard";
// import RecentActivity from "../components/dashboard/RecentActivity";
// import ContractsTable from "../components/dashboard/ContractsTable";
// import RiskChart from "../components/dashboard/RiskChart";
// import ContractDetails from "../components/dashboard/ContractDetails";
// import QuickActions from "../components/dashboard/QuickActions";

// function Dashboard() {
//   const stats = [
//     {
//       title: "Total Contracts",
//       value: 12,
//       color: "#2563eb",
//     },
//     {
//       title: "High Risk Clauses",
//       value: 5,
//       color: "#dc2626",
//     },
//     {
//       title: "Medium Risk Clauses",
//       value: 14,
//       color: "#ca8a04",
//     },
//     {
//       title: "Low Risk Clauses",
//       value: 22,
//       color: "#16a34a",
//     },
//   ];

//   return (
//     <Layout>
//       <div className="mb-8">
//         <h1 className="text-4xl font-bold mb-2">
//           AI Contract Dashboard
//         </h1>

//         <p className="text-gray-600">
//           Monitor contracts, risks, and AI analysis.
//         </p>
//       </div>

//       <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
//         {stats.map((item, index) => (
//           <StatsCard
//             key={index}
//             title={item.title}
//             value={item.value}
//             color={item.color}
//           />
//         ))}
//       </div>
//       <RecentActivity />
//       <ContractsTable />
//       <RiskChart />
//       <ContractDetails />
//       <QuickActions />
//     </Layout>
//   );
// }

// export default Dashboard;

// recently updated dashboard.jsx file

// import Layout from "../components/layout/Layout";
// import StatsCard from "../components/dashboard/StatsCard";
// import RecentActivity from "../components/dashboard/RecentActivity";
// import ContractsTable from "../components/dashboard/ContractsTable";
// import RiskChart from "../components/dashboard/RiskChart";
// import ContractDetails from "../components/dashboard/ContractDetails";
// import QuickActions from "../components/dashboard/QuickActions";

// function Dashboard() {
//   const stats = [
//     {
//       title: "Total Contracts",
//       value: 12,
//       color: "#2563eb",
//       icon: "📄",
//       change: "+12%",
//       bg: "from-blue-600 to-indigo-600",
//     },
//     {
//       title: "High Risk Clauses",
//       value: 5,
//       color: "#dc2626",
//       icon: "⚠️",
//       change: "-2%",
//       bg: "from-red-500 to-rose-600",
//     },
//     {
//       title: "Medium Risk Clauses",
//       value: 14,
//       color: "#ca8a04",
//       icon: "🟡",
//       change: "+5%",
//       bg: "from-amber-500 to-orange-500",
//     },
//     {
//       title: "Low Risk Clauses",
//       value: 22,
//       color: "#16a34a",
//       icon: "✅",
//       change: "+18%",
//       bg: "from-emerald-500 to-green-600",
//     },
//   ];

//   return (
//     <Layout>
//       <section className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
//         <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
//           <div>
//             <div className="mb-4 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-blue-100">
//               AI Contract Intelligence Dashboard
//             </div>

//             <h1 className="text-4xl font-bold tracking-tight lg:text-5xl">
//               Welcome Back 👋
//             </h1>

//             <p className="mt-3 max-w-2xl text-slate-300">
//               Monitor uploaded contracts, legal risks, clause predictions,
//               chatbot activity, and AI-powered analysis from one workspace.
//             </p>
//           </div>

//           <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
//             <p className="text-sm text-blue-100">System Status</p>
//             <h3 className="mt-1 text-2xl font-bold text-green-300">
//               Active
//             </h3>
//             <p className="mt-1 text-sm text-slate-300">
//               Backend APIs connected
//             </p>
//           </div>
//         </div>
//       </section>

//       <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
//         {stats.map((item, index) => (
//           <div
//             key={index}
//             className={`rounded-3xl bg-gradient-to-br ${item.bg} p-[1px] shadow-lg transition hover:-translate-y-1 hover:shadow-2xl`}
//           >
//             <div className="h-full rounded-3xl bg-white p-6">
//               <div className="mb-5 flex items-center justify-between">
//                 <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-2xl">
//                   {item.icon}
//                 </div>

//                 <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
//                   {item.change}
//                 </span>
//               </div>

//               <p className="text-sm font-semibold text-slate-500">
//                 {item.title}
//               </p>

//               <h2 className="mt-2 text-4xl font-bold text-slate-900">
//                 {item.value}
//               </h2>
//             </div>
//           </div>
//         ))}
//       </section>

//       <div className="mt-8 space-y-8">
//         <RecentActivity />
//         <ContractsTable />
//         <RiskChart />
//         <ContractDetails />
//         <QuickActions />
//       </div>
//     </Layout>
//   );
// }

// export default Dashboard;




// import { useEffect, useState } from "react";
// import Layout from "../components/layout/Layout";
// import RecentActivity from "../components/dashboard/RecentActivity";
// import ContractsTable from "../components/dashboard/ContractsTable";
// import RiskChart from "../components/dashboard/RiskChart";
// import ContractDetails from "../components/dashboard/ContractDetails";
// import QuickActions from "../components/dashboard/QuickActions";
// import { getContracts } from "../services/api";

// function Dashboard() {
//   const [contracts, setContracts] = useState([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     fetchDashboardData();
//   }, []);

//   const fetchDashboardData = async () => {
//     try {
//       setLoading(true);
//       const data = await getContracts();
//       setContracts(Array.isArray(data) ? data : data?.contracts || []);
//     } catch (error) {
//       console.log("Dashboard contracts error:", error);
//       setContracts([]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const stats = [
//     {
//       title: "Total Contracts",
//       value: contracts.length,
//       icon: "📄",
//       change: "Live",
//       bg: "from-blue-600 to-indigo-600",
//     },
//     {
//       title: "Uploaded",
//       value: contracts.filter((item) => item.status === "uploaded").length,
//       icon: "✅",
//       change: "Live",
//       bg: "from-emerald-500 to-green-600",
//     },
//     {
//       title: "Processing",
//       value: contracts.filter(
//         (item) =>
//           item.status === "processing" ||
//           item.status === "analyzing"
//       ).length,
//       icon: "⏳",
//       change: "Live",
//       bg: "from-amber-500 to-orange-500",
//     },
//     {
//       title: "Failed",
//       value: contracts.filter((item) => item.status === "failed").length,
//       icon: "⚠️",
//       change: "Live",
//       bg: "from-red-500 to-rose-600",
//     },
//   ];

//   const latestContract = contracts[0] || null;

//   return (
//     <Layout>
//       <section className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
//         <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
//           <div>
//             <div className="mb-4 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-blue-100">
//               AI Contract Intelligence Dashboard
//             </div>

//             <h1 className="text-4xl font-bold tracking-tight lg:text-5xl">
//               Welcome Back 👋
//             </h1>

//             <p className="mt-3 max-w-2xl text-slate-300">
//               Monitor uploaded contracts, legal risks, clause predictions,
//               chatbot activity, and AI-powered analysis from one workspace.
//             </p>
//           </div>

//           <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
//             <p className="text-sm text-blue-100">System Status</p>
//             <h3 className="mt-1 text-2xl font-bold text-green-300">
//               {loading ? "Checking..." : "Active"}
//             </h3>
//             <p className="mt-1 text-sm text-slate-300">
//               Backend APIs connected
//             </p>
//           </div>
//         </div>
//       </section>

//       <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
//         {stats.map((item, index) => (
//           <div
//             key={index}
//             className={`rounded-3xl bg-gradient-to-br ${item.bg} p-[1px] shadow-lg transition hover:-translate-y-1 hover:shadow-2xl`}
//           >
//             <div className="h-full rounded-3xl bg-white dark:bg-slate-900 p-6">
//               <div className="mb-5 flex items-center justify-between">
//                 <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 dark:bg-slate-800 text-2xl">
//                   {item.icon}
//                 </div>

//                 <span className="rounded-full bg-slate-100 dark:bg-slate-800 px-3 py-1 text-xs font-semibold text-slate-600 dark:text-slate-300">
//                   {item.change}
//                 </span>
//               </div>

//               <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">
//                 {item.title}
//               </p>

//               <h2 className="mt-2 text-4xl font-bold text-slate-900 dark:text-white">
//                 {loading ? "..." : item.value}
//               </h2>
//             </div>
//           </div>
//         ))}
//       </section>

//       <div className="mt-8 space-y-8">
//         <RecentActivity contracts={contracts} />
//         <ContractsTable contracts={contracts} loading={loading} />
//         <RiskChart contracts={contracts} />
//         <ContractDetails contract={latestContract} />
//         <QuickActions />
//       </div>
//     </Layout>
//   );
// }

// export default Dashboard;


import { useEffect, useState } from "react";
import Layout from "../components/layout/Layout";
import RecentActivity from "../components/dashboard/RecentActivity";
import ContractsTable from "../components/dashboard/ContractsTable";
import RiskChart from "../components/dashboard/RiskChart";
import ContractDetails from "../components/dashboard/ContractDetails";
import QuickActions from "../components/dashboard/QuickActions";
import { getContracts } from "../services/api";

function Dashboard() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    const handleDashboardSearch = (e) => {
      setSearchQuery(e.detail || "");
    };

    window.addEventListener("dashboard-search", handleDashboardSearch);

    return () => {
      window.removeEventListener(
        "dashboard-search",
        handleDashboardSearch
      );
    };
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const data = await getContracts();
      setContracts(Array.isArray(data) ? data : data?.contracts || []);
    } catch (error) {
      console.log("Dashboard contracts error:", error);
      setContracts([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredContracts = contracts.filter((contract) => {
    const query = searchQuery.toLowerCase();

    return (
      contract.filename?.toLowerCase().includes(query) ||
      contract.status?.toLowerCase().includes(query) ||
      contract.contract_id?.toLowerCase().includes(query)
    );
  });

  const stats = [
    {
      title: "Total Contracts",
      value: filteredContracts.length,
      icon: "📄",
      change: searchQuery ? "Filtered" : "Live",
      bg: "from-blue-600 to-indigo-600",
    },
    {
      title: "Uploaded",
      value: filteredContracts.filter(
        (item) => item.status === "uploaded"
      ).length,
      icon: "✅",
      change: searchQuery ? "Filtered" : "Live",
      bg: "from-emerald-500 to-green-600",
    },
    {
      title: "Processing",
      value: filteredContracts.filter(
        (item) =>
          item.status === "processing" ||
          item.status === "analyzing"
      ).length,
      icon: "⏳",
      change: searchQuery ? "Filtered" : "Live",
      bg: "from-amber-500 to-orange-500",
    },
    {
      title: "Failed",
      value: filteredContracts.filter(
        (item) => item.status === "failed"
      ).length,
      icon: "⚠️",
      change: searchQuery ? "Filtered" : "Live",
      bg: "from-red-500 to-rose-600",
    },
  ];

  const latestContract = filteredContracts[0] || null;

  return (
    <Layout>
      <section className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-900 p-8 text-white shadow-xl">
        <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
          <div>
            <div className="mb-4 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-blue-100">
              AI Contract Intelligence Dashboard
            </div>

            <h1 className="text-4xl font-bold tracking-tight lg:text-5xl">
              Welcome Back 👋
            </h1>

            <p className="mt-3 max-w-2xl text-slate-300">
              Monitor uploaded contracts, legal risks, clause predictions,
              chatbot activity, and AI-powered analysis from one workspace.
            </p>

            {searchQuery && (
              <p className="mt-4 inline-flex rounded-full bg-white/10 px-4 py-2 text-sm text-blue-100">
                Showing results for: {searchQuery}
              </p>
            )}
          </div>

          <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
            <p className="text-sm text-blue-100">System Status</p>
            <h3 className="mt-1 text-2xl font-bold text-green-300">
              {loading ? "Checking..." : "Active"}
            </h3>
            <p className="mt-1 text-sm text-slate-300">
              Backend APIs connected
            </p>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((item, index) => (
          <div
            key={index}
            className={`rounded-3xl bg-gradient-to-br ${item.bg} p-[1px] shadow-lg transition hover:-translate-y-1 hover:shadow-2xl`}
          >
            <div className="h-full rounded-3xl bg-white dark:bg-slate-900 p-6">
              <div className="mb-5 flex items-center justify-between">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 dark:bg-slate-800 text-2xl">
                  {item.icon}
                </div>

                <span className="rounded-full bg-slate-100 dark:bg-slate-800 px-3 py-1 text-xs font-semibold text-slate-600 dark:text-slate-300">
                  {item.change}
                </span>
              </div>

              <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">
                {item.title}
              </p>

              <h2 className="mt-2 text-4xl font-bold text-slate-900 dark:text-white">
                {loading ? "..." : item.value}
              </h2>
            </div>
          </div>
        ))}
      </section>

      <div className="mt-8 space-y-8">
        <RecentActivity contracts={filteredContracts} />
        <ContractsTable contracts={filteredContracts} loading={loading} />
        <RiskChart contracts={filteredContracts} />
        <ContractDetails contract={latestContract} />
        <QuickActions />
      </div>
    </Layout>
  );
}

export default Dashboard;