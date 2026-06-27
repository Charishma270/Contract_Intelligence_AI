// import { Link } from "react-router-dom";
// import { Mail, ArrowLeft } from "lucide-react";

// function ForgotPassword() {
//   const handleSubmit = (e) => {
//     e.preventDefault();

//     alert("Password reset link sent! (Demo)");
//   };

//   return (
//     <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">

//       {/* LEFT PANEL */}
//       <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
//         <div className="max-w-lg text-white">

//           <div className="mb-6 inline-block rounded-full bg-blue-500/20 px-4 py-2 text-sm text-blue-200">
//             Password Recovery
//           </div>

//           <h1 className="text-5xl font-bold mb-6 leading-tight">
//             Reset Your Password Securely
//           </h1>

//           <p className="text-lg text-slate-300">
//             Enter your registered email address and we'll send you a password reset link.
//           </p>

//         </div>
//       </div>

//       {/* RIGHT PANEL */}
//       <div className="flex w-full lg:w-1/2 items-center justify-center p-6">

//         <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">

//           <Link
//             to="/login"
//             className="inline-flex items-center gap-2 text-blue-600 mb-6 hover:underline"
//           >
//             <ArrowLeft size={18} />
//             Back to Login
//           </Link>

//           <h2 className="text-3xl font-bold mb-2">
//             Forgot Password
//           </h2>

//           <p className="text-slate-500 mb-8">
//             We'll email you a password reset link.
//           </p>

//           <form
//             onSubmit={handleSubmit}
//             className="space-y-6"
//           >

//             <div>
//               <label className="block text-sm font-semibold mb-2">
//                 Email Address
//               </label>

//               <div className="relative">

//                 <Mail
//                   size={18}
//                   className="absolute left-4 top-4 text-slate-400"
//                 />

//                 <input
//                   type="email"
//                   placeholder="Enter your email"
//                   className="w-full rounded-xl border border-slate-300 pl-12 pr-4 py-3 outline-none focus:border-blue-600"
//                 />

//               </div>
//             </div>

//             <button
//               className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition"
//             >
//               Send Reset Link
//             </button>

//           </form>

//           <p className="mt-6 text-center text-sm text-slate-500">
//             Remember your password?{" "}
//             <Link
//               to="/login"
//               className="font-semibold text-blue-600"
//             >
//               Login
//             </Link>
//           </p>

//         </div>

//       </div>

//     </div>
//   );
// }

// export default ForgotPassword;


// import { useState } from "react";
// import { Link } from "react-router-dom";
// import { Mail, ArrowLeft, Loader2, CheckCircle, AlertCircle } from "lucide-react";
// import { forgotPasswordApi } from "../services/api";

// function ForgotPassword() {
//   const [email, setEmail] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState("");
//   const [error, setError] = useState("");

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!email.trim()) {
//       setError("Please enter your email address.");
//       return;
//     }

//     try {
//       setLoading(true);
//       setError("");
//       setMessage("");

//       const data = await forgotPasswordApi(email);

//       setMessage(
//         data?.message || "Password reset instructions sent to your email."
//       );
//     } catch (err) {
//       setError(
//         err.response?.data?.detail ||
//           err.response?.data?.message ||
//           "Unable to send reset link. Please try again."
//       );
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
//       <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
//         <div className="max-w-lg text-white">
//           <div className="mb-6 inline-block rounded-full bg-blue-500/20 px-4 py-2 text-sm text-blue-200">
//             Password Recovery
//           </div>

//           <h1 className="text-5xl font-bold mb-6 leading-tight">
//             Reset Your Password Securely
//           </h1>

//           <p className="text-lg text-slate-300">
//             Enter your registered email address and we&apos;ll send you password reset instructions.
//           </p>
//         </div>
//       </div>

//       <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
//         <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
//           <Link
//             to="/login"
//             className="inline-flex items-center gap-2 text-blue-600 mb-6 hover:underline"
//           >
//             <ArrowLeft size={18} />
//             Back to Login
//           </Link>

//           <h2 className="text-3xl font-bold mb-2">Forgot Password</h2>

//           <p className="text-slate-500 mb-8">
//             We&apos;ll email you password reset instructions.
//           </p>

//           {message && (
//             <div className="mb-5 flex items-center gap-2 rounded-xl bg-green-50 px-4 py-3 text-sm font-semibold text-green-700">
//               <CheckCircle size={18} />
//               {message}
//             </div>
//           )}

//           {error && (
//             <div className="mb-5 flex items-center gap-2 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
//               <AlertCircle size={18} />
//               {error}
//             </div>
//           )}

//           <form onSubmit={handleSubmit} className="space-y-6">
//             <div>
//               <label className="block text-sm font-semibold mb-2">
//                 Email Address
//               </label>

//               <div className="relative">
//                 <Mail
//                   size={18}
//                   className="absolute left-4 top-4 text-slate-400"
//                 />

//                 <input
//                   type="email"
//                   value={email}
//                   onChange={(e) => setEmail(e.target.value)}
//                   placeholder="Enter your email"
//                   className="w-full rounded-xl border border-slate-300 pl-12 pr-4 py-3 outline-none focus:border-blue-600"
//                 />
//               </div>
//             </div>

//             <button
//               disabled={loading}
//               className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:bg-slate-400 transition"
//             >
//               {loading ? (
//                 <span className="flex items-center justify-center gap-2">
//                   <Loader2 size={18} className="animate-spin" />
//                   Sending...
//                 </span>
//               ) : (
//                 "Send Reset Link"
//               )}
//             </button>
//           </form>

//           <p className="mt-6 text-center text-sm text-slate-500">
//             Remember your password?{" "}
//             <Link to="/login" className="font-semibold text-blue-600">
//               Login
//             </Link>
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default ForgotPassword;

import { useState } from "react";
import { Link } from "react-router-dom";
import {
  Mail,
  ArrowLeft,
  Loader2,
  CheckCircle,
  AlertCircle,
  KeyRound,
  Eye,
  EyeOff,
} from "lucide-react";
import {
  forgotPasswordApi,
  resetPasswordApi,
} from "../services/api";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [resetToken, setResetToken] = useState("");

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [resetLoading, setResetLoading] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSendToken = async (e) => {
    e.preventDefault();

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");
      setResetToken("");

      const data = await forgotPasswordApi(email);

      setMessage(data?.message || "Reset token generated.");

      if (data?.reset_token) {
        setResetToken(data.reset_token);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.message ||
          "Unable to generate reset token."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();

    if (!resetToken || !newPassword || !confirmPassword) {
      setError("Please fill all reset password fields.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("New password and confirm password do not match.");
      return;
    }

    try {
      setResetLoading(true);
      setError("");
      setMessage("");

      const data = await resetPasswordApi({
        token: resetToken,
        newPassword,
        confirmPassword,
      });

      setMessage(data?.message || "Password reset successful.");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.message ||
          "Password reset failed."
      );
    } finally {
      setResetLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
        <div className="max-w-lg text-white">
          <div className="mb-6 inline-block rounded-full bg-blue-500/20 px-4 py-2 text-sm text-blue-200">
            Password Recovery
          </div>

          <h1 className="text-5xl font-bold mb-6 leading-tight">
            Reset Your Password Securely
          </h1>

          <p className="text-lg text-slate-300">
            Generate a reset token and create a new password.
          </p>
        </div>
      </div>

      <div className="flex w-full lg:w-1/2 items-center justify-center p-6">
        <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
          <Link
            to="/login"
            className="inline-flex items-center gap-2 text-blue-600 mb-6 hover:underline"
          >
            <ArrowLeft size={18} />
            Back to Login
          </Link>

          <h2 className="text-3xl font-bold mb-2">
            Forgot Password
          </h2>

          <p className="text-slate-500 mb-8">
            Enter your email to generate a reset token.
          </p>

          {message && (
            <div className="mb-5 flex items-start gap-2 rounded-xl bg-green-50 px-4 py-3 text-sm font-semibold text-green-700">
              <CheckCircle size={18} />
              <span>{message}</span>
            </div>
          )}

          {error && (
            <div className="mb-5 flex items-start gap-2 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSendToken} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold mb-2">
                Email Address
              </label>

              <div className="relative">
                <Mail
                  size={18}
                  className="absolute left-4 top-4 text-slate-400"
                />

                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full rounded-xl border border-slate-300 pl-12 pr-4 py-3 outline-none focus:border-blue-600"
                />
              </div>
            </div>

            <button
              disabled={loading}
              className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:bg-slate-400 transition"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 size={18} className="animate-spin" />
                  Generating...
                </span>
              ) : (
                "Generate Reset Token"
              )}
            </button>
          </form>

          {resetToken && (
            <form
              onSubmit={handleResetPassword}
              className="mt-8 space-y-5 border-t pt-6"
            >
              <div>
                <label className="block text-sm font-semibold mb-2">
                  Reset Token
                </label>

                <div className="relative">
                  <KeyRound
                    size={18}
                    className="absolute left-4 top-4 text-slate-400"
                  />

                  <input
                    type="text"
                    value={resetToken}
                    onChange={(e) => setResetToken(e.target.value)}
                    className="w-full rounded-xl border border-slate-300 pl-12 pr-4 py-3 outline-none focus:border-blue-600"
                  />
                </div>
              </div>

              <PasswordInput
                label="New Password"
                value={newPassword}
                setValue={setNewPassword}
                show={showNewPassword}
                setShow={setShowNewPassword}
              />

              <PasswordInput
                label="Confirm Password"
                value={confirmPassword}
                setValue={setConfirmPassword}
                show={showConfirmPassword}
                setShow={setShowConfirmPassword}
              />

              <button
                disabled={resetLoading}
                className="w-full rounded-xl bg-green-600 py-3 font-semibold text-white hover:bg-green-700 disabled:bg-slate-400 transition"
              >
                {resetLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 size={18} className="animate-spin" />
                    Resetting...
                  </span>
                ) : (
                  "Reset Password"
                )}
              </button>
            </form>
          )}

          <p className="mt-6 text-center text-sm text-slate-500">
            Remember your password?{" "}
            <Link to="/login" className="font-semibold text-blue-600">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

function PasswordInput({ label, value, setValue, show, setShow }) {
  return (
    <div>
      <label className="block text-sm font-semibold mb-2">
        {label}
      </label>

      <div className="relative">
        <input
          type={show ? "text" : "password"}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={label}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-blue-600"
        />

        <button
          type="button"
          onClick={() => setShow(!show)}
          className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-blue-600"
        >
          {show ? <EyeOff size={20} /> : <Eye size={20} />}
        </button>
      </div>
    </div>
  );
}

export default ForgotPassword;