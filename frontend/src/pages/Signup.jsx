// import { useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { Eye, EyeOff } from "lucide-react";

// function Signup() {
//   const navigate = useNavigate();

//   const [showPassword, setShowPassword] = useState(false);
//   const [showConfirmPassword, setShowConfirmPassword] =
//     useState(false);

//   const handleSignup = (e) => {
//     e.preventDefault();

//     // Temporary frontend-only signup
//     navigate("/dashboard");
//   };

//   return (
//     <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900">
//       <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
//         <div className="max-w-lg text-white">
//           <div className="mb-6 inline-block rounded-full bg-indigo-500/20 px-4 py-2 text-sm text-indigo-200">
//             Secure Contract Intelligence
//           </div>

//           <h1 className="text-5xl font-bold leading-tight mb-6">
//             Start Managing Legal Risk with AI
//           </h1>

//           <p className="text-lg text-slate-300 mb-8">
//             Create your workspace to upload contracts, analyze clauses, and
//             interact with your legal documents through AI.
//           </p>

//           <div className="rounded-2xl bg-white/10 p-6 backdrop-blur">
//             <p className="text-slate-200">
//               Built for legal, compliance, and contract review teams.
//             </p>
//           </div>
//         </div>
//       </div>

//       <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
//         <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
//           <h2 className="text-3xl font-bold text-slate-900 mb-2">
//             Create Account
//           </h2>

//           <p className="text-slate-500 mb-8">
//             Sign up to access Contract Intelligence AI.
//           </p>

//           <form onSubmit={handleSignup} className="space-y-5">
//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Full Name
//               </label>

//               <input
//                 type="text"
//                 placeholder="Enter your name"
//                 className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-indigo-600"
//               />
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Email Address
//               </label>

//               <input
//                 type="email"
//                 placeholder="Enter your email"
//                 className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-indigo-600"
//               />
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Password
//               </label>

//               <div className="relative">
//                 <input
//                   type={showPassword ? "text" : "password"}
//                   placeholder="Create password"
//                   className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-indigo-600"
//                 />

//                 <button
//                   type="button"
//                   onClick={() => setShowPassword(!showPassword)}
//                   className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-indigo-600"
//                 >
//                   {showPassword ? (
//                     <EyeOff size={20} />
//                   ) : (
//                     <Eye size={20} />
//                   )}
//                 </button>
//               </div>
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Confirm Password
//               </label>

//               <div className="relative">
//                 <input
//                   type={
//                     showConfirmPassword ? "text" : "password"
//                   }
//                   placeholder="Confirm password"
//                   className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-indigo-600"
//                 />

//                 <button
//                   type="button"
//                   onClick={() =>
//                     setShowConfirmPassword(
//                       !showConfirmPassword
//                     )
//                   }
//                   className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-indigo-600"
//                 >
//                   {showConfirmPassword ? (
//                     <EyeOff size={20} />
//                   ) : (
//                     <Eye size={20} />
//                   )}
//                 </button>
//               </div>
//             </div>

//             <button className="w-full rounded-xl bg-indigo-600 py-3 font-semibold text-white hover:bg-indigo-700 transition">
//               Create Account
//             </button>
//           </form>

//           <p className="text-center text-sm text-slate-600 mt-6">
//             Already have an account?{" "}
//             <Link to="/login" className="font-semibold text-indigo-600">
//               Login
//             </Link>
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Signup;




// import { useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { Eye, EyeOff } from "lucide-react";
// import { useAuth } from "../context/AuthContext";

// function Signup() {
//   const navigate = useNavigate();
//   const { signup } = useAuth();

//   const [showPassword, setShowPassword] = useState(false);
//   const [showConfirmPassword, setShowConfirmPassword] = useState(false);

//   const [name, setName] = useState("");
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState("");

//   const [error, setError] = useState("");

//   const handleSignup = async (e) => {
//     e.preventDefault();

//     if (!name || !email || !password || !confirmPassword) {
//       setError("Please fill all fields.");
//       return;
//     }

//     if (password !== confirmPassword) {
//       setError("Passwords do not match.");
//       return;
//     }

//     const result = await signup({
//       name,
//       email,
//       password,
//     });

//     if (!result.success) {
//       setError(result.message);
//       return;
//     }

//     navigate("/dashboard");
//   };

//   return (
//     <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900">
//       <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
//         <div className="max-w-lg text-white">
//           <div className="mb-6 inline-block rounded-full bg-indigo-500/20 px-4 py-2 text-sm text-indigo-200">
//             Secure Contract Intelligence
//           </div>

//           <h1 className="text-5xl font-bold leading-tight mb-6">
//             Start Managing Legal Risk with AI
//           </h1>

//           <p className="text-lg text-slate-300 mb-8">
//             Create your workspace to upload contracts, analyze clauses, and
//             interact with your legal documents through AI.
//           </p>

//           <div className="rounded-2xl bg-white/10 p-6 backdrop-blur">
//             <p className="text-slate-200">
//               Built for legal, compliance, and contract review teams.
//             </p>
//           </div>
//         </div>
//       </div>

//       <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
//         <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
//           <h2 className="text-3xl font-bold text-slate-900 mb-2">
//             Create Account
//           </h2>

//           <p className="text-slate-500 mb-8">
//             Sign up to access Contract Intelligence AI.
//           </p>

//           <form onSubmit={handleSignup} className="space-y-5">
//             {error && (
//               <div className="rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">
//                 {error}
//               </div>
//             )}

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Full Name
//               </label>

//               <input
//                 type="text"
//                 value={name}
//                 onChange={(e) => setName(e.target.value)}
//                 placeholder="Enter your name"
//                 className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-indigo-600"
//               />
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Email Address
//               </label>

//               <input
//                 type="email"
//                 value={email}
//                 onChange={(e) => setEmail(e.target.value)}
//                 placeholder="Enter your email"
//                 className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-indigo-600"
//               />
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Password
//               </label>

//               <div className="relative">
//                 <input
//                   type={showPassword ? "text" : "password"}
//                   value={password}
//                   onChange={(e) => setPassword(e.target.value)}
//                   placeholder="Create password"
//                   className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-indigo-600"
//                 />

//                 <button
//                   type="button"
//                   onClick={() => setShowPassword(!showPassword)}
//                   className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-indigo-600"
//                 >
//                   {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
//                 </button>
//               </div>
//             </div>

//             <div>
//               <label className="block text-sm font-semibold text-slate-700 mb-2">
//                 Confirm Password
//               </label>

//               <div className="relative">
//                 <input
//                   type={showConfirmPassword ? "text" : "password"}
//                   value={confirmPassword}
//                   onChange={(e) => setConfirmPassword(e.target.value)}
//                   placeholder="Confirm password"
//                   className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-indigo-600"
//                 />

//                 <button
//                   type="button"
//                   onClick={() =>
//                     setShowConfirmPassword(!showConfirmPassword)
//                   }
//                   className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-indigo-600"
//                 >
//                   {showConfirmPassword ? (
//                     <EyeOff size={20} />
//                   ) : (
//                     <Eye size={20} />
//                   )}
//                 </button>
//               </div>
//             </div>

//             <button className="w-full rounded-xl bg-indigo-600 py-3 font-semibold text-white hover:bg-indigo-700 transition">
//               Create Account
//             </button>
//           </form>

//           <p className="text-center text-sm text-slate-600 mt-6">
//             Already have an account?{" "}
//             <Link to="/login" className="font-semibold text-indigo-600">
//               Login
//             </Link>
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Signup;



import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import { useAuth } from "../context/AuthContext";

function Signup() {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();

    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill all fields.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    setError("");

    const result = await signup({
      name,
      email,
      password,
    });

    setLoading(false);

    if (!result.success) {
      setError(result.message);
      return;
    }

    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900">
      <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
        <div className="max-w-lg text-white">
          <div className="mb-6 inline-block rounded-full bg-indigo-500/20 px-4 py-2 text-sm text-indigo-200">
            Secure Contract Intelligence
          </div>

          <h1 className="text-5xl font-bold leading-tight mb-6">
            Start Managing Legal Risk with AI
          </h1>

          <p className="text-lg text-slate-300 mb-8">
            Create your workspace to upload contracts, analyze clauses, and
            interact with your legal documents through AI.
          </p>

          <div className="rounded-2xl bg-white/10 p-6 backdrop-blur">
            <p className="text-slate-200">
              Built for legal, compliance, and contract review teams.
            </p>
          </div>
        </div>
      </div>

      <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
        <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
          <h2 className="text-3xl font-bold text-slate-900 mb-2">
            Create Account
          </h2>

          <p className="text-slate-500 mb-8">
            Sign up to access Contract Intelligence AI.
          </p>

          <form onSubmit={handleSignup} className="space-y-5">
            {error && (
              <div className="rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Full Name
              </label>

              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-indigo-600"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Email Address
              </label>

              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-indigo-600"
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
                  placeholder="Create password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-indigo-600"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-indigo-600"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Confirm Password
              </label>

              <div className="relative">
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  value={confirmPassword}
                  onChange={(e) =>
                    setConfirmPassword(e.target.value)
                  }
                  placeholder="Confirm password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-indigo-600"
                />

                <button
                  type="button"
                  onClick={() =>
                    setShowConfirmPassword(
                      !showConfirmPassword
                    )
                  }
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-indigo-600"
                >
                  {showConfirmPassword ? (
                    <EyeOff size={20} />
                  ) : (
                    <Eye size={20} />
                  )}
                </button>
              </div>
            </div>

            <button
              disabled={loading}
              className="w-full rounded-xl bg-indigo-600 py-3 font-semibold text-white hover:bg-indigo-700 disabled:bg-slate-400 transition"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>
          </form>

          <p className="text-center text-sm text-slate-600 mt-6">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-semibold text-indigo-600"
            >
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Signup;