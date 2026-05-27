// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://localhost:8000"
// });

// export const analyzeClause = async (query) => {
//   const response = await API.post("/analyze", {
//     query
//   });

//   return response.data;
// };

//week 3 wedddd

import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const analyzeClause = async (query) => {
  const response = await API.post("/api/rag/rag/analyze", {
    query,
  });

  return response.data;
};

export const uploadContract = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await API.post("/api/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};