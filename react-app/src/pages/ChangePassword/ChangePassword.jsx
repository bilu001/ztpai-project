import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import milan from "../../assets/milan.png"

export default function ChangePassword() {

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();
  

  async function handleSubmit(e) {
    e.preventDefault();
  
    if (newPassword !== confirmPassword) {
      alert("New password and confirmation do not match!");
      return;
    }
  
    try {
      const response = await fetch("http://localhost:8000/change_password/", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Error changing password");
      }
  
      const data = await response.json();
      console.log("Password changed successfully:", data);
      navigate("/player-dashboard");
    } catch (err) {
      console.error(err.message);
      alert(err.message);
    }
  }
  
  return (
    <div className="flex min-h-screen">
      <div className="w-full md:w-1/2 bg-white flex flex-col justify-center p-8">
        <h2 className="text-xl mb-2 font-semibold">Player dashboard login page</h2>
        <h3 className="text-lg mb-6">Change your password</h3>

        <form onSubmit={handleSubmit} className="max-w-sm space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="currentPassword">
              Current Password
            </label>
            <input
              id="currentPassword"
              type="password"
              placeholder="Enter your password"
              className="border border-gray-300 rounded w-full p-2"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="newPassword">
              New Password
            </label>
            <input
              id="newPassword"
              type="password"
              placeholder="Enter your new password"
              className="border border-gray-300 rounded w-full p-2"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="confirmPassword">
              Confirm New Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              placeholder="Enter your new password"
              className="border border-gray-300 rounded w-full p-2"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="bg-red-600 hover:bg-red-700 text-white w-full py-2 rounded"
          >
            Login now
          </button>
        </form>
      </div>
      <div className="hidden md:flex md:w-1/2 bg-gray-800 text-white flex-col items-center justify-center p-8">
        <h2 className="text-3xl mb-4">AC MILAN</h2>
        <img
          src={milan}
          alt="AC Milan Logo"
          className="h-40 mb-8"
        />
        <p className="max-w-sm text-center">
          Saremo una squadra di diavoli. I nostri colori saranno il rosso come il fuoco 
          e il nero come la paura che incuteremo agli avversari!
        </p>
      </div>
    </div>
  );
}
