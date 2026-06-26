function AIOptions() {

  const options = [
    "Clause Detection",
    "Risk Analysis",
    "Entity Extraction",
    "AI Summary",
  ];

  return (
    <div className="bg-white rounded-3xl shadow-lg p-8">

      <h2 className="text-2xl font-bold mb-6">
        AI Processing Options
      </h2>

      <div className="grid md:grid-cols-2 gap-5">

        {options.map((item,index)=>(

          <label
            key={index}
            className="flex items-center gap-4 p-5 rounded-2xl bg-slate-50 hover:bg-blue-50 cursor-pointer"
          >

            <input
              type="checkbox"
              defaultChecked
              className="w-5 h-5"
            />

            <span className="font-medium">
              {item}
            </span>

          </label>

        ))}

      </div>

    </div>
  );
}

export default AIOptions;