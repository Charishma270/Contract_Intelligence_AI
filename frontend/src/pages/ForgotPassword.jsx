import { Link } from "react-router-dom";
import { Mail, ArrowLeft } from "lucide-react";

function ForgotPassword() {
  const handleSubmit = (e) => {
    e.preventDefault();

    alert("Password reset link sent! (Demo)");
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">

      {/* LEFT PANEL */}
      <div className="hidden lg:flex w-1/2 items-center justify-center p-12">
        <div className="max-w-lg text-white">

          <div className="mb-6 inline-block rounded-full bg-blue-500/20 px-4 py-2 text-sm text-blue-200">
            Password Recovery
          </div>

          <h1 className="text-5xl font-bold mb-6 leading-tight">
            Reset Your Password Securely
          </h1>

          <p className="text-lg text-slate-300">
            Enter your registered email address and we'll send you a password reset link.
          </p>

        </div>
      </div>

      {/* RIGHT PANEL */}
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
            We'll email you a password reset link.
          </p>

          <form
            onSubmit={handleSubmit}
            className="space-y-6"
          >

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
                  placeholder="Enter your email"
                  className="w-full rounded-xl border border-slate-300 pl-12 pr-4 py-3 outline-none focus:border-blue-600"
                />

              </div>
            </div>

            <button
              className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 transition"
            >
              Send Reset Link
            </button>

          </form>

          <p className="mt-6 text-center text-sm text-slate-500">
            Remember your password?{" "}
            <Link
              to="/login"
              className="font-semibold text-blue-600"
            >
              Login
            </Link>
          </p>

        </div>

      </div>

    </div>
  );
}

export default ForgotPassword;