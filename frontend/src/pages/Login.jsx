// import { useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { Eye, EyeOff } from "lucide-react";

// function Login() {
//   const navigate = useNavigate();
//   const [showPassword, setShowPassword] = useState(false);

//   const handleLogin = (e) => {
//     e.preventDefault();

//     // Temporary frontend-only login
//     navigate("/dashboard");
//   };

//   return (
//     <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
//       <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
//         <div className="max-w-lg text-white">
//           <div className="mb-6 inline-block rounded-full bg-blue-500/20 px-4 py-2 text-sm text-blue-200">
//             AI Legal Intelligence Platform
//           </div>

//           <h1 className="text-5xl font-bold leading-tight mb-6">
//             Analyze Contracts Smarter with AI
//           </h1>

//           <p className="text-lg text-slate-300 mb-8">
//             Upload contracts, detect legal clauses, score risks, and ask
//             intelligent questions using a contract-aware AI assistant.
//           </p>

//           <div className="grid grid-cols-2 gap-4">
//             <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
//               <h3 className="text-2xl font-bold">41+</h3>
//               <p className="text-sm text-slate-300">Clause Categories</p>
//             </div>

//             <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
//               <h3 className="text-2xl font-bold">AI</h3>
//               <p className="text-sm text-slate-300">Risk Scoring</p>
//             </div>
//           </div>
//         </div>
//       </div>

//       <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
//         <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
//           <h2 className="text-3xl font-bold text-slate-900 mb-2">
//             Welcome Back
//           </h2>

//           <p className="text-slate-500 mb-8">
//             Login to continue to Contract Intelligence AI.
//           </p>

//           <form onSubmit={handleLogin} className="space-y-5">
//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Email Address
//               </label>

//               <input
//                 type="email"
//                 placeholder="Enter your email"
//                 className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-600"
//               />
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Password
//               </label>

//               <div className="relative">
//                 <input
//                   type={showPassword ? "text" : "password"}
//                   placeholder="Enter your password"
//                   className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-blue-600"
//                 />

//                 <button
//                   type="button"
//                   onClick={() => setShowPassword(!showPassword)}
//                   className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-blue-600"
//                 >
//                   {showPassword ? (
//                     <EyeOff size={20} />
//                   ) : (
//                     <Eye size={20} />
//                   )}
//                 </button>
//               </div>
//             </div>

//             <div className="flex items-center justify-between text-sm">
//   <label className="flex items-center gap-2 text-slate-600">
//     <input type="checkbox" />
//     Remember me
//   </label>

//   <Link
//     to="/forgot-password"
//     className="text-blue-600 font-medium hover:text-blue-700 hover:underline transition"
//   >
//     Forgot Password?
//   </Link>
// </div>

//             <button className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition">
//               Login
//             </button>
//           </form>

//           <p className="text-center text-sm text-slate-600 mt-6">
//             Don&apos;t have an account?{" "}
//             <Link to="/signup" className="font-semibold text-blue-600">
//               Sign up
//             </Link>
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Login;




import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import { useAuth } from "../context/AuthContext";

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError("Please enter email and password.");
      return;
    }

    const result = login(email, password);

    if (!result.success) {
      setError(result.message);
      return;
    }

    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
        <div className="max-w-lg text-white">
          <div className="mb-6 inline-block rounded-full bg-blue-500/20 px-4 py-2 text-sm text-blue-200">
            AI Legal Intelligence Platform
          </div>

          <h1 className="text-5xl font-bold leading-tight mb-6">
            Analyze Contracts Smarter with AI
          </h1>

          <p className="text-lg text-slate-300 mb-8">
            Upload contracts, detect legal clauses, score risks, and ask
            intelligent questions using a contract-aware AI assistant.
          </p>

          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
              <h3 className="text-2xl font-bold">41+</h3>
              <p className="text-sm text-slate-300">Clause Categories</p>
            </div>

            <div className="rounded-2xl bg-white/10 p-5 backdrop-blur">
              <h3 className="text-2xl font-bold">AI</h3>
              <p className="text-sm text-slate-300">Risk Scoring</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
        <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
          <h2 className="text-3xl font-bold text-slate-900 mb-2">
            Welcome Back
          </h2>

          <p className="text-slate-500 mb-8">
            Login to continue to Contract Intelligence AI.
          </p>

          <form onSubmit={handleLogin} className="space-y-5">
            {error && (
              <div className="rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Email Address
              </label>

              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-600"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Password
              </label>

              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-blue-600"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-blue-600"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 text-slate-600">
                <input type="checkbox" />
                Remember me
              </label>

              <Link
                to="/forgot-password"
                className="text-blue-600 font-medium hover:text-blue-700 hover:underline transition"
              >
                Forgot Password?
              </Link>
            </div>

            <button className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition">
              Login
            </button>
          </form>

          <p className="text-center text-sm text-slate-600 mt-6">
            Don&apos;t have an account?{" "}
            <Link to="/signup" className="font-semibold text-blue-600">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;