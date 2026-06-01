function RecentActivity() {
  const activities = [
    "Contract uploaded successfully",
    "Termination clause analyzed",
    "Chatbot queried for confidentiality",
    "Risk scoring completed",
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">
      <h2 className="text-2xl font-bold mb-5">
        Recent Activity
      </h2>

      <div className="space-y-4">
        {activities.map((activity, index) => (
          <div
            key={index}
            className="border-b pb-3 text-gray-700"
          >
            • {activity}
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentActivity;