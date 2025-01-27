import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ReportInjury() {
  const [username, setUsername] = useState("");
  const [playerId, setPlayerId] = useState(null);
  const [type, setType] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [feelings, setFeelings] = useState("");
  const [nextVisit, setNextVisit] = useState("");
  const navigate = useNavigate();

  async function fetchPlayerId() {
    try {
      const res = await fetch(`http://localhost:8000/api/get-player-id-by-username/${username}/`);
      if (!res.ok) throw new Error("Player not found");
      const data = await res.json();
      setPlayerId(data.player_id); // Save player_id in state
      alert("Player ID fetched successfully!");
    } catch (err) {
      console.error(err.message);
      alert(err.message);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (!playerId) {
      alert("Please fetch the Player ID before submitting the form.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/report_injury/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          player_id: playerId,
          type,
          location,
          description,
          feelings,
          next_visit: nextVisit,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to report injury");
      }

      alert("Injury reported successfully!");
      navigate("/player-dashboard");
    } catch (err) {
      console.error(err.message);
      alert(err.message);
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Report an Injury</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">Username</label>
          <div className="flex gap-2">
            <input
              type="text"
              className="border p-2 w-full"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <button
              type="button"
              className="bg-blue-600 text-white px-4 py-2 rounded"
              onClick={fetchPlayerId} // Fetch Player ID on button click
            >
              Get Player ID
            </button>
          </div>
        </div>

        <div>
          <label className="block mb-1">Type of Injury</label>
          <input
            type="text"
            className="border p-2 w-full"
            value={type}
            onChange={(e) => setType(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block mb-1">Location</label>
          <input
            type="text"
            className="border p-2 w-full"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block mb-1">Description</label>
          <textarea
            className="border p-2 w-full"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block mb-1">Feelings</label>
          <textarea
            className="border p-2 w-full"
            value={feelings}
            onChange={(e) => setFeelings(e.target.value)}
          />
        </div>
        <div>
          <label className="block mb-1">Next Visit</label>
          <input
            type="date"
            className="border p-2 w-full"
            value={nextVisit}
            onChange={(e) => setNextVisit(e.target.value)}
          />
        </div>
        <button className="bg-green-600 text-white px-4 py-2 rounded">Submit</button>
      </form>
    </div>
  );
}
