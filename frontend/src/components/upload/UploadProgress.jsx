function UploadProgress() {
  return (
    <div className="bg-white rounded-3xl shadow-lg p-8">

      <div className="flex justify-between mb-3">

        <h2 className="text-xl font-bold">
          Upload Progress
        </h2>

        <span className="font-semibold text-blue-600">
          72%
        </span>

      </div>

      <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">

        <div
          className="bg-blue-600 h-full rounded-full"
          style={{ width: "72%" }}
        ></div>

      </div>

    </div>
  );
}

export default UploadProgress;