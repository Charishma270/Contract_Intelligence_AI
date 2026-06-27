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

// import axios from "axios";

// // In Docker (behind nginx proxy): leave VITE_API_BASE_URL unset → relative URLs
// // For local dev: set VITE_API_BASE_URL=http://localhost:8000 in frontend/.env
// const API = axios.create({
//   baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
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

// export const getContracts = async () => {
//   const response = await API.get("/api/contracts");
//   return response.data;
// };


// export const chatWithContract = async (
//   contractId,
//   question
// ) => {
//   const response = await API.post("/api/chat/chat", {
//     contract_id: contractId,
//     query: question,
//   });

//   return response.data;
// };





// import axios from "axios";

// const API = axios.create({
//   baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
// });

// // Attach JWT token automatically to protected requests
// API.interceptors.request.use(
//   (config) => {
//     const token =
//   localStorage.getItem("token") ||
//   sessionStorage.getItem("token");

//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }

//     return config;
//   },
//   (error) => Promise.reject(error)
// );

// // Optional: handle expired/invalid token globally
// API.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       localStorage.removeItem("token");
//       localStorage.removeItem("currentUser");
//     }

//     return Promise.reject(error);
//   }
// );

// // -------------------- AUTH --------------------

// export const signupUser = async (userData) => {
//   const response = await API.post("/api/auth/signup", userData);
//   return response.data;
// };

// export const loginUser = async (credentials) => {
//   const response = await API.post("/api/auth/login", credentials);
//   return response.data;
// };

// export const logoutUser = async () => {
//   const response = await API.post("/api/auth/logout");
//   return response.data;
// };

// export const getCurrentUser = async () => {
//   const response = await API.get("/api/auth/me");
//   return response.data;
// };

// // -------------------- PROFILE --------------------

// export const getProfile = async () => {
//   const response = await API.get("/api/profile/");
//   return response.data;
// };

// export const updateProfileApi = async (profileData) => {
//   const response = await API.put("/api/profile/", profileData);
//   return response.data;
// };

// export const changePasswordApi = async (passwordData) => {
//   const response = await API.put(
//     "/api/profile/change-password",
//     passwordData
//   );

//   return response.data;
// };

// // -------------------- TWO FACTOR --------------------

// export const setupTwoFactor = async () => {
//   const response = await API.post("/api/auth/2fa/setup");
//   return response.data;
// };

// export const verifyTwoFactor = async (code) => {
//   const response = await API.post("/api/auth/2fa/verify", {
//     code,
//   });

//   return response.data;
// };

// export const loginWithTwoFactor = async (code) => {
//   const response = await API.post("/api/auth/2fa/login", {
//     code,
//   });

//   return response.data;
// };

// export const disableTwoFactor = async (code) => {
//   const response = await API.post("/api/auth/2fa/disable", {
//     code,
//   });

//   return response.data;
// };

// // -------------------- CONTRACT / ANALYSIS --------------------

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

// export const getContracts = async () => {
//   const response = await API.get("/api/contracts");
//   return response.data;
// };

// export const chatWithContract = async (contractId, question) => {
//   const response = await API.post("/api/chat/chat", {
//     contract_id: contractId,
//     query: question,
//   });

//   return response.data;
// };

// export default API;



import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

// Attach JWT token automatically
API.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("token") ||
      sessionStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Handle expired / invalid token
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("currentUser");

      sessionStorage.removeItem("token");
      sessionStorage.removeItem("currentUser");

      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

// -------------------- AUTH --------------------

export const signupUser = async (userData) => {
  const response = await API.post("/api/auth/signup", userData);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await API.post("/api/auth/login", credentials);
  return response.data;
};

export const logoutUser = async () => {
  const response = await API.post("/api/auth/logout");
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await API.get("/api/auth/me");
  return response.data;
};

// -------------------- PROFILE --------------------

export const getProfile = async () => {
  const response = await API.get("/api/profile/");
  return response.data;
};

export const updateProfileApi = async (profileData) => {
  const response = await API.put("/api/profile/", profileData);
  return response.data;
};

export const changePasswordApi = async (passwordData) => {
  const response = await API.put(
    "/api/profile/change-password",
    passwordData
  );

  return response.data;
};

// -------------------- TWO FACTOR --------------------

export const setupTwoFactor = async () => {
  const response = await API.post("/api/auth/2fa/setup");
  return response.data;
};

export const verifyTwoFactor = async (code) => {
  const response = await API.post("/api/auth/2fa/verify", {
    code,
  });

  return response.data;
};

export const loginWithTwoFactor = async (code) => {
  const response = await API.post("/api/auth/2fa/login", {
    code,
  });

  return response.data;
};

export const disableTwoFactor = async (code) => {
  const response = await API.post("/api/auth/2fa/disable", {
    code,
  });

  return response.data;
};

// -------------------- CONTRACT / ANALYSIS --------------------

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

export const chatWithContract = async (contractId, question) => {
  const response = await API.post("/api/chat/chat", {
    contract_id: contractId,
    query: question,
  });

  return response.data;
};


export const forgotPasswordApi = async (email) => {
  const response = await API.post("/api/auth/forgot-password", {
    email,
  });

  return response.data;
};

export default API;


