import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import acMilanLogo from "../../assets/milan.png"; 

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        //credentials: "include",
        body: JSON.stringify({ username, password }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Login failed");
      }
      const data = await response.json();
      console.log("Login success:", data);
      if (data.role === "coach") {
        navigate("/coach-dashboard");
      }
      else if (data.role === "player") {
        if (data.force_password_change) {
          navigate("/change-password");
        } else {
          navigate("/player-dashboard");
        } 
      } else {
        alert("You are not a coach nor a player!");
      }
      } catch (err) {
        console.error(err.message);
        alert(err.message);
      }
  };

  return (
    <div className="flex min-h-screen">
      <div className="w-full md:w-1/2 bg-white flex flex-col justify-center items-center p-8">
        <h1 className="text-2xl font-bold mb-6">Dashboard login page</h1>
        <form onSubmit={handleLogin} className="max-w-sm space-y-4">
          <div>
            <label className="block text-sm font-semibold mb-1" htmlFor="username">
              Username
            </label>
            <input
              id="username"
              type="username"
              placeholder="username"
              className="w-full border border-gray-300 rounded px-3 py-2"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold mb-1" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              className="w-full border border-gray-300 rounded px-3 py-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <a 
              href="#"
              className="text-sm text-blue-600 hover:underline inline-block mt-2"
              onClick={() => alert("Forgot password clicked!")}
            >
              Forgot password?
            </a>
          </div>
          <button
            type="submit"
            className="bg-red-600 hover:bg-red-700 text-white font-semibold px-6 py-2 rounded mt-2"
          >
            Login now
          </button>
        </form>
      </div>
      <div className="hidden md:flex md:w-1/2 bg-gray-900 text-white flex-col items-center justify-center p-8">
        <h2 className="text-3xl font-bold mb-4">AC MILAN</h2>
        <img
          src={acMilanLogo}
          alt="AC Milan Logo"
          className="h-40 w-auto mb-8"
        />
        <p className="max-w-md text-center leading-relaxed">
          Saremo una squadra di diavoli. I nostri colori saranno il rosso come il fuoco 
          e il nero come la paura che incuteremo agli avversari!
        </p>
      </div>
    </div>
  );
}
