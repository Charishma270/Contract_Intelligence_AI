function StatsCard({
  title,
  value,
  color,
}) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border-l-4"
      style={{ borderColor: color }}
    >
      <h3 className="text-gray-500 text-sm font-medium mb-2">
        {title}
      </h3>

      <p className="text-3xl font-bold">
        {value}
      </p>
    </div>
  );
}

export default StatsCard;