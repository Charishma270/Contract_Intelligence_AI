import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const analyzeClause = async (query) => {
  const response = await API.post("/analyze", {
    query
  });

  return response.data;
};
