import Layout from "../components/layout/Layout";

function Dashboard() {
  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-4">Dashboard Overview</h2>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 shadow rounded">
          Total Contracts
        </div>

        <div className="bg-white p-4 shadow rounded">
          Risk Score
        </div>

        <div className="bg-white p-4 shadow rounded">
          Entities Extracted
        </div>
      </div>
    </Layout>
  );
}

export default Dashboard;