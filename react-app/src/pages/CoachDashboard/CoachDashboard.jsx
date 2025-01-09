import React, { useState, useEffect } from "react";
import Navbar from "../Navbar";

export default function CoachDashboard() {
  const [players, setPlayers] = useState([ ]);
  
  const [showModal, setShowModal] = useState(false);
  const [newName, setNewName] = useState("");
  const [newSurname, setNewSurname] = useState("");
  const [newRole, setNewRole] = useState("Striker"); 
  const [newContractEnd, setNewContractEnd] = useState("");

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setNewName("");
    setNewSurname("");
    setNewRole("Striker");
    setNewContractEnd("");
  };

  useEffect(() => {
    async function fetchPlayers() {
      try {
        const res = await fetch("http://localhost:8000/api/players/");
        if (!res.ok) throw new Error("Failed to fetch players");
        const data = await res.json();
        setPlayers(data);
      } catch (err) {
        console.error(err);
        alert(err.message);
      }
    }
    fetchPlayers();
  }, []);

  async function handleAddPlayer(e) {
    e.preventDefault();
    try {
      // Build FormData instead of JSON
      const formData = new FormData();
      formData.append("name", newName);
      formData.append("surname", newSurname);
      formData.append("role", newRole);
      formData.append("contract_end", newContractEnd);
    
      const response = await fetch("http://localhost:8000/api/add_player/", {
        method: "POST",
        body: formData,
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to add player");
      }
  
      const data = await response.json();
      console.log("Player added:", data);
      setPlayers((prev) => [...prev, data.player]);
  
      handleCloseModal();
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  }

  useEffect(() => {
    fetchPlayers();
  }, []);

  async function fetchPlayers() {
    try {
      const res = await fetch("http://localhost:8000/api/players/");
      if (!res.ok) throw new Error("Failed to fetch players");
      const data = await res.json();
      setPlayers(data);
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  }

  async function handleRemovePlayer(playerId) {
    try {
      const res = await fetch(`http://localhost:8000/api/remove_player/${playerId}/`, {
        method: "DELETE",
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Failed to remove player");
      }
      setPlayers(prev => prev.filter(p => p.player_id !== playerId));
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  }

  return (
    <div className="bg-white min-h-screen">
      <Navbar />
      <div className="p-8">
        <h1 className="text-3xl font-bold mb-6">COACH DASHBOARD</h1>
        <button
          className="bg-green-700 text-white px-4 py-2 rounded mb-6 hover:bg-green-800"
          onClick={handleOpenModal}
        >
          Add a new player
        </button>
        {showModal && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-6 rounded shadow-md max-w-md w-full">
              <h2 className="text-xl font-bold mb-4">Add New Player</h2>
              <form onSubmit={handleAddPlayer} className="space-y-4">
                <div>
                  <label className="block mb-1">Name</label>
                  <input
                    type="text"
                    className="border p-2 w-full"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block mb-1">Surname</label>
                  <input
                    type="text"
                    className="border p-2 w-full"
                    value={newSurname}
                    onChange={(e) => setNewSurname(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block mb-1">Role</label>
                  <select
                    className="border p-2 w-full"
                    value={newRole}
                    onChange={(e) => setNewRole(e.target.value)}
                  >
                    <option value="Striker">Striker</option>
                    <option value="Defender">Defender</option>
                    <option value="Midfielder">Midfielder</option>
                    <option value="Goalkeeper">Goalkeeper</option>
                  </select>
                </div>
                <div>
                  <label className="block mb-1">Contract ends</label>
                  <input
                    type="date"
                    className="border p-2 w-full"
                    value={newContractEnd}
                    onChange={(e) => setNewContractEnd(e.target.value)}
                  />
                </div>
                <div>
              </div>
                <div className="flex gap-4 mt-4">
                  <button
                    type="submit"
                    className="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-800"
                  >
                    Save
                  </button>
                  <button
                    type="button"
                    className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
                    onClick={handleCloseModal}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
        <div className="space-y-4">
          {players.map((player) => (
            <div
              key={player.id}
              className={`p-4 flex items-center justify-between ${
                player.id % 2 === 1 ? "bg-red-600" : "bg-black"
              } text-white rounded`}
            >
              <div className="flex items-center">
                <div>
                  <p className="text-lg font-semibold">{player.name} {player.surname}</p>
                  <p>{player.position}</p>
                  <p>Contract valid until: {player.contract_ends}</p>
                </div>
              </div>
              <div className="flex gap-3">
                <button className="bg-white text-black px-3 py-1 rounded hover:bg-gray-200">
                  Add statistics
                </button>
                <button className="bg-white text-black px-3 py-1 rounded hover:bg-gray-200" onClick={() => handleRemovePlayer(player.player_id)}>
                  Remove player
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
