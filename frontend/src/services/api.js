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

// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://localhost:8000",
// });

// export const analyzeClause = async (query) => {
//   const response = await API.post("/api/rag/rag/analyze", {
//     query,
//   });

//   return response.data;
// };

// export const uploadContract = async (file) => {
//   const formData = new FormData();
//   formData.append("file", file);

//   const response = await API.post("/api/upload", formData, {
//     headers: {
//       "Content-Type": "multipart/form-data",
//     },
//   });

//   return response.data;
// };

//week 4 thursdayyyyyyy

import axios from "axios";

// In Docker (behind nginx proxy): leave VITE_API_BASE_URL unset → relative URLs
// For local dev: set VITE_API_BASE_URL=http://localhost:8000 in frontend/.env
const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
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

export const getContracts = async () => {
  const response = await API.get("/api/contracts");
  return response.data;
};

// export const chatWithContract = async (question) => {
//   const response = await API.post("/api/chat/chat", {
//     contract_id: "eb490748-2268-478c-ba40-f7319f10ff59",
//     query: question,
//   });

//   return response.data;
// };

export const chatWithContract = async (
  contractId,
  question
) => {
  const response = await API.post("/api/chat/chat", {
    contract_id: contractId,
    query: question,
  });

  return response.data;
};
