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
    <div>
      <h1>Welcome to Home Page</h1>
      {token ? (
        <>
          <p>Logged in with token: {token}</p>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <p>You are not logged in.</p>
          <button onClick={() => navigate("/login")}>Go to Login</button>
        </>
      )}
    </div>
  );
}
