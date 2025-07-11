import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const [token, setToken] = useState(null);

  useEffect(() => {
    const accessToken = localStorage.getItem("access");
    setToken(accessToken);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200">
      <div className="card w-96 bg-base-100 shadow-xl p-8 space-y-4 text-center">
        <h1 className="text-2xl font-bold">Welcome to Home Page</h1>

        {token ? (
          <>
            <p className="text-sm break-words text-neutral-600">
              Logged in with token:
              <br />
              <code className="text-xs break-all">{token}</code>
            </p>
            <button className="btn btn-error w-full" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <p className="text-neutral-600">You are not logged in.</p>
            <div className="flex flex-col gap-2">
              <button
                className="btn btn-primary w-full"
                onClick={() => navigate("/login")}
              >
                Go to Login
              </button>
              <button
                className="btn btn-secondary w-full"
                onClick={() => navigate("/register")}
              >
                Sign Up
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
