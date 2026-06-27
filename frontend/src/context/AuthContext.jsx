// import { createContext, useContext, useEffect, useState } from "react";

// const AuthContext = createContext();

// export function AuthProvider({ children }) {
//   const [currentUser, setCurrentUser] = useState(() => {
//     const savedUser = localStorage.getItem("currentUser");
//     return savedUser ? JSON.parse(savedUser) : null;
//   });

//   useEffect(() => {
//     if (currentUser) {
//       localStorage.setItem("currentUser", JSON.stringify(currentUser));
//     } else {
//       localStorage.removeItem("currentUser");
//     }
//   }, [currentUser]);

//   const signup = (userData) => {
//     const users = JSON.parse(localStorage.getItem("users")) || [];

//     const userExists = users.find(
//       (user) => user.email === userData.email
//     );

//     if (userExists) {
//       return {
//         success: false,
//         message: "Account already exists. Please login.",
//       };
//     }

//     const newUser = {
//       id: Date.now(),
//       name: userData.name,
//       email: userData.email,
//       password: userData.password,
//       role: "Frontend Developer",
//       organization: "Zaalima Development Ltd.",
//       phone: "+91 98765 43210",
//       joinedDate: "June 2026",
//       lastLogin: "Today",
//     };

//     localStorage.setItem("users", JSON.stringify([...users, newUser]));
//     setCurrentUser(newUser);

//     return {
//       success: true,
//       message: "Signup successful.",
//     };
//   };

//   const login = (email, password) => {
//     const users = JSON.parse(localStorage.getItem("users")) || [];

//     const user = users.find(
//       (item) => item.email === email && item.password === password
//     );

//     if (!user) {
//       return {
//         success: false,
//         message: "Invalid email or password.",
//       };
//     }

//     setCurrentUser({
//       ...user,
//       lastLogin: "Today",
//     });

//     return {
//       success: true,
//       message: "Login successful.",
//     };
//   };

//   const logout = () => {
//     setCurrentUser(null);
//   };

//   return (
//     <AuthContext.Provider value={{ currentUser, signup, login, logout }}>
//       {children}
//     </AuthContext.Provider>
//   );
// }

// export function useAuth() {
//   return useContext(AuthContext);
// }





// import {
//   createContext,
//   useContext,
//   useEffect,
//   useState,
// } from "react";

// const AuthContext = createContext();

// export function AuthProvider({ children }) {
//   const [currentUser, setCurrentUser] = useState(() => {
//     const savedUser = localStorage.getItem("currentUser");
//     return savedUser ? JSON.parse(savedUser) : null;
//   });

//   useEffect(() => {
//     if (currentUser) {
//       localStorage.setItem(
//         "currentUser",
//         JSON.stringify(currentUser)
//       );
//     } else {
//       localStorage.removeItem("currentUser");
//     }
//   }, [currentUser]);

//   const getUsers = () => {
//     return JSON.parse(localStorage.getItem("users")) || [];
//   };

//   const saveUsers = (users) => {
//     localStorage.setItem("users", JSON.stringify(users));
//   };

//   const signup = (userData) => {
//     const users = getUsers();

//     const userExists = users.find(
//       (user) => user.email === userData.email
//     );

//     if (userExists) {
//       return {
//         success: false,
//         message: "Account already exists. Please login.",
//       };
//     }

//     const newUser = {
//       id: Date.now(),
//       name: userData.name,
//       email: userData.email,
//       password: userData.password,
//       role: "Frontend Developer",
//       organization: "Zaalima Development Ltd.",
//       phone: "+91 98765 43210",
//       joinedDate: "June 2026",
//       lastLogin: "Today",
//     };

//     saveUsers([...users, newUser]);
//     setCurrentUser(newUser);

//     return {
//       success: true,
//       message: "Signup successful.",
//     };
//   };

//   const login = (email, password) => {
//     const users = getUsers();

//     const user = users.find(
//       (item) =>
//         item.email === email && item.password === password
//     );

//     if (!user) {
//       return {
//         success: false,
//         message: "Invalid email or password.",
//       };
//     }

//     const updatedUser = {
//       ...user,
//       lastLogin: "Today",
//     };

//     setCurrentUser(updatedUser);

//     return {
//       success: true,
//       message: "Login successful.",
//     };
//   };

//   const updateProfile = (updatedData) => {
//     if (!currentUser) {
//       return {
//         success: false,
//         message: "No logged-in user found.",
//       };
//     }

//     const users = getUsers();

//     const emailTaken = users.find(
//       (user) =>
//         user.email === updatedData.email &&
//         user.id !== currentUser.id
//     );

//     if (emailTaken) {
//       return {
//         success: false,
//         message: "This email is already used by another account.",
//       };
//     }

//     const updatedUser = {
//       ...currentUser,
//       ...updatedData,
//     };

//     const updatedUsers = users.map((user) =>
//       user.id === currentUser.id ? updatedUser : user
//     );

//     saveUsers(updatedUsers);
//     setCurrentUser(updatedUser);

//     return {
//       success: true,
//       message: "Profile updated successfully.",
//     };
//   };

//   const changePassword = ({
//     currentPassword,
//     newPassword,
//     confirmPassword,
//   }) => {
//     if (!currentUser) {
//       return {
//         success: false,
//         message: "No logged-in user found.",
//       };
//     }

//     if (!currentPassword || !newPassword || !confirmPassword) {
//       return {
//         success: false,
//         message: "Please fill all password fields.",
//       };
//     }

//     if (currentUser.password !== currentPassword) {
//       return {
//         success: false,
//         message: "Current password is incorrect.",
//       };
//     }

//     if (newPassword !== confirmPassword) {
//       return {
//         success: false,
//         message: "New password and confirm password do not match.",
//       };
//     }

//     if (newPassword.length < 6) {
//       return {
//         success: false,
//         message: "Password must be at least 6 characters.",
//       };
//     }

//     const updatedUser = {
//       ...currentUser,
//       password: newPassword,
//     };

//     const users = getUsers();

//     const updatedUsers = users.map((user) =>
//       user.id === currentUser.id ? updatedUser : user
//     );

//     saveUsers(updatedUsers);
//     setCurrentUser(updatedUser);

//     return {
//       success: true,
//       message: "Password updated successfully.",
//     };
//   };

//   const logout = () => {
//     setCurrentUser(null);
//   };

//   return (
//     <AuthContext.Provider
//       value={{
//         currentUser,
//         signup,
//         login,
//         updateProfile,
//         changePassword,
//         logout,
//       }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// }

// export function useAuth() {
//   return useContext(AuthContext);
// }





// import {
//   createContext,
//   useContext,
//   useEffect,
//   useState,
// } from "react";

// import {
//   signupUser,
//   loginUser,
//   logoutUser,
//   getCurrentUser,
//   updateProfileApi,
//   changePasswordApi,
// } from "../services/api";

// const AuthContext = createContext();

// export function AuthProvider({ children }) {
//   const [currentUser, setCurrentUser] = useState(() => {
//     const savedUser = localStorage.getItem("currentUser");
//     return savedUser ? JSON.parse(savedUser) : null;
//   });

//   const [authLoading, setAuthLoading] = useState(true);

//   useEffect(() => {
//     const loadLoggedInUser = async () => {
//       const token = localStorage.getItem("token");

//       if (!token) {
//         setCurrentUser(null);
//         setAuthLoading(false);
//         return;
//       }

//       try {
//         const data = await getCurrentUser();

//         if (data?.success && data?.user) {
//           setCurrentUser(data.user);
//           localStorage.setItem(
//             "currentUser",
//             JSON.stringify(data.user)
//           );
//         }
//       } catch (error) {
//         localStorage.removeItem("token");
//         localStorage.removeItem("currentUser");
//         setCurrentUser(null);
//       } finally {
//         setAuthLoading(false);
//       }
//     };

//     loadLoggedInUser();
//   }, []);

//   const signup = async (userData) => {
//     try {
//       const data = await signupUser(userData);

//       if (data?.token) {
//         localStorage.setItem("token", data.token);
//       }

//       if (data?.user) {
//         setCurrentUser(data.user);
//         localStorage.setItem(
//           "currentUser",
//           JSON.stringify(data.user)
//         );
//       }

//       return {
//         success: true,
//         message: data?.message || "Signup successful.",
//         requires_2fa: data?.requires_2fa || false,
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Signup failed. Please try again.",
//       };
//     }
//   };

//   const login = async (email, password) => {
//     try {
//       const data = await loginUser({
//         email,
//         password,
//       });

//       if (data?.token) {
//         localStorage.setItem("token", data.token);
//       }

//       if (data?.user) {
//         setCurrentUser(data.user);
//         localStorage.setItem(
//           "currentUser",
//           JSON.stringify(data.user)
//         );
//       }

//       return {
//         success: true,
//         message: data?.message || "Login successful.",
//         requires_2fa: data?.requires_2fa || false,
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Invalid email or password.",
//       };
//     }
//   };

//   const updateProfile = async (updatedData) => {
//     try {
//       const data = await updateProfileApi(updatedData);

//       if (data?.user) {
//         setCurrentUser(data.user);
//         localStorage.setItem(
//           "currentUser",
//           JSON.stringify(data.user)
//         );
//       }

//       return {
//         success: true,
//         message:
//           data?.message || "Profile updated successfully.",
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Profile update failed.",
//       };
//     }
//   };

//   const changePassword = async (passwordData) => {
//     try {
//       const data = await changePasswordApi(passwordData);

//       return {
//         success: true,
//         message:
//           data?.message || "Password updated successfully.",
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Password update failed.",
//       };
//     }
//   };

//   const logout = async () => {
//     try {
//       await logoutUser();
//     } catch (error) {
//       console.log("Logout API error:", error);
//     } finally {
//       localStorage.removeItem("token");
//       localStorage.removeItem("currentUser");
//       setCurrentUser(null);
//     }
//   };

//   return (
//     <AuthContext.Provider
//       value={{
//         currentUser,
//         authLoading,
//         signup,
//         login,
//         updateProfile,
//         changePassword,
//         logout,
//       }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// }

// export function useAuth() {
//   return useContext(AuthContext);
// }


// import {
//   createContext,
//   useContext,
//   useEffect,
//   useState,
// } from "react";

// import {
//   signupUser,
//   loginUser,
//   logoutUser,
//   getCurrentUser,
//   updateProfileApi,
//   changePasswordApi,
// } from "../services/api";

// const AuthContext = createContext();

// export function AuthProvider({ children }) {
//   const [currentUser, setCurrentUser] = useState(() => {
//     const savedLocalUser = localStorage.getItem("currentUser");
//     const savedSessionUser = sessionStorage.getItem("currentUser");

//     if (savedLocalUser) return JSON.parse(savedLocalUser);
//     if (savedSessionUser) return JSON.parse(savedSessionUser);

//     return null;
//   });

//   const [authLoading, setAuthLoading] = useState(true);

//   const saveAuthData = (token, user, rememberMe = true) => {
//     localStorage.removeItem("token");
//     localStorage.removeItem("currentUser");
//     sessionStorage.removeItem("token");
//     sessionStorage.removeItem("currentUser");

//     const storage = rememberMe ? localStorage : sessionStorage;

//     if (token) {
//       storage.setItem("token", token);
//     }

//     if (user) {
//       storage.setItem("currentUser", JSON.stringify(user));
//       setCurrentUser(user);
//     }
//   };

//   const clearAuthData = () => {
//     localStorage.removeItem("token");
//     localStorage.removeItem("currentUser");
//     sessionStorage.removeItem("token");
//     sessionStorage.removeItem("currentUser");
//     setCurrentUser(null);
//   };

//   const getStoredToken = () => {
//     return (
//       localStorage.getItem("token") ||
//       sessionStorage.getItem("token")
//     );
//   };

//   const getRememberMode = () => {
//     return Boolean(localStorage.getItem("token"));
//   };

//   useEffect(() => {
//     const loadLoggedInUser = async () => {
//       const token = getStoredToken();

//       if (!token) {
//         clearAuthData();
//         setAuthLoading(false);
//         return;
//       }

//       try {
//         const data = await getCurrentUser();

//         if (data?.success && data?.user) {
//           const rememberMode = getRememberMode();
//           saveAuthData(token, data.user, rememberMode);
//         }
//       } catch (error) {
//         clearAuthData();
//       } finally {
//         setAuthLoading(false);
//       }
//     };

//     loadLoggedInUser();
//   }, []);

//   const signup = async (userData) => {
//     try {
//       const data = await signupUser(userData);

//       if (data?.token && data?.user) {
//         saveAuthData(data.token, data.user, true);
//       }

//       return {
//         success: true,
//         message: data?.message || "Signup successful.",
//         requires_2fa: data?.requires_2fa || false,
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Signup failed. Please try again.",
//       };
//     }
//   };

//   const login = async (email, password, rememberMe = false) => {
//     try {
//       const data = await loginUser({
//         email,
//         password,
//       });

//       if (data?.token && data?.user) {
//         saveAuthData(data.token, data.user, rememberMe);
//       }

//       return {
//         success: true,
//         message: data?.message || "Login successful.",
//         requires_2fa: data?.requires_2fa || false,
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Invalid email or password.",
//       };
//     }
//   };

//   const updateProfile = async (updatedData) => {
//     try {
//       const data = await updateProfileApi(updatedData);

//       if (data?.user) {
//         const token = getStoredToken();
//         const rememberMode = getRememberMode();

//         saveAuthData(token, data.user, rememberMode);
//       }

//       return {
//         success: true,
//         message:
//           data?.message || "Profile updated successfully.",
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Profile update failed.",
//       };
//     }
//   };

//   const changePassword = async (passwordData) => {
//     try {
//       const data = await changePasswordApi(passwordData);

//       return {
//         success: true,
//         message:
//           data?.message || "Password updated successfully.",
//       };
//     } catch (error) {
//       return {
//         success: false,
//         message:
//           error.response?.data?.detail ||
//           "Password update failed.",
//       };
//     }
//   };

//   const logout = async () => {
//     try {
//       await logoutUser();
//     } catch (error) {
//       console.log("Logout API error:", error);
//     } finally {
//       clearAuthData();
//     }
//   };

//   return (
//     <AuthContext.Provider
//       value={{
//         currentUser,
//         authLoading,
//         signup,
//         login,
//         updateProfile,
//         changePassword,
//         logout,
//       }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// }

// export function useAuth() {
//   return useContext(AuthContext);
// }


import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import {
  signupUser,
  loginUser,
  logoutUser,
  getCurrentUser,
  updateProfileApi,
  changePasswordApi,
} from "../services/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(() => {
    const savedLocalUser = localStorage.getItem("currentUser");
    const savedSessionUser = sessionStorage.getItem("currentUser");

    if (savedLocalUser) return JSON.parse(savedLocalUser);
    if (savedSessionUser) return JSON.parse(savedSessionUser);

    return null;
  });

  const [authLoading, setAuthLoading] = useState(true);

  const getStoredToken = () => {
    return (
      localStorage.getItem("token") ||
      sessionStorage.getItem("token")
    );
  };

  const getRememberMode = () => {
    return Boolean(localStorage.getItem("token"));
  };

  const saveAuthData = (token, user, rememberMe = true) => {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("currentUser");

    const storage = rememberMe ? localStorage : sessionStorage;

    if (token) {
      storage.setItem("token", token);
    }

    if (user) {
      storage.setItem("currentUser", JSON.stringify(user));
    }

    setCurrentUser(user || null);
  };

  const clearAuthData = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("currentUser");
    setCurrentUser(null);
  };

  useEffect(() => {
    const loadLoggedInUser = async () => {
      const token = getStoredToken();

      if (!token) {
        clearAuthData();
        setAuthLoading(false);
        return;
      }

      try {
        const data = await getCurrentUser();

        if (data?.user) {
          const rememberMode = getRememberMode();
          saveAuthData(token, data.user, rememberMode);
        } else {
          clearAuthData();
        }
      } catch (error) {
        clearAuthData();
      } finally {
        setAuthLoading(false);
      }
    };

    loadLoggedInUser();
  }, []);

  const signup = async (userData) => {
    try {
      const data = await signupUser(userData);

      const token =
        data?.token ||
        data?.access_token ||
        data?.accessToken;

      const user =
        data?.user ||
        data?.data?.user ||
        data?.profile;

      if (token && user) {
        saveAuthData(token, user, true);
      }

      return {
        success: true,
        message: data?.message || "Signup successful.",
        requires_2fa: data?.requires_2fa || false,
      };
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Signup failed. Please try again.",
      };
    }
  };

  const login = async (email, password, rememberMe = false) => {
    try {
      const data = await loginUser({
        email,
        password,
      });

      const token =
        data?.token ||
        data?.access_token ||
        data?.accessToken;

      const user =
        data?.user ||
        data?.data?.user ||
        data?.profile;

      if (token && user) {
        saveAuthData(token, user, rememberMe);
      }

      return {
        success: true,
        message: data?.message || "Login successful.",
        requires_2fa: data?.requires_2fa || false,
      };
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Invalid email or password.",
      };
    }
  };

  const updateProfile = async (updatedData) => {
    try {
      const data = await updateProfileApi(updatedData);

      const user =
        data?.user ||
        data?.data?.user ||
        data?.profile ||
        data;

      if (user) {
        const token = getStoredToken();
        const rememberMode = getRememberMode();
        saveAuthData(token, user, rememberMode);
      }

      return {
        success: true,
        message:
          data?.message || "Profile updated successfully.",
      };
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Profile update failed.",
      };
    }
  };

  const changePassword = async (passwordData) => {
    try {
      const data = await changePasswordApi(passwordData);

      return {
        success: true,
        message:
          data?.message || "Password updated successfully.",
      };
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Password update failed.",
      };
    }
  };

  const logout = async () => {
    try {
      await logoutUser();
    } catch (error) {
      console.log("Logout API error:", error);
    } finally {
      clearAuthData();
    }
  };

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        authLoading,
        signup,
        login,
        updateProfile,
        changePassword,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}