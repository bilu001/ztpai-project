import React from "react";
import Navbar from "../Navbar";

export default function PlayerDashboard() {
  const lastMatchStats = {
    goals: 2,
    assists: 1,
    distance: "10km",
    // ...
    overall: 7.3,
  };

  return (
    <div className="bg-gray-900 min-h-screen text-white">
      <Navbar />
      <div className="p-6">
        <h1 className="text-2xl mb-4">Welcome back!</h1>

        <div className="bg-gray-800 p-4 mb-6 rounded">
          <h2 className="text-xl font-bold mb-2">Last match statistics and feedback</h2>
          <div className="grid grid-cols-2 gap-4 mb-2">
            <p>Goals: {lastMatchStats.goals}</p>
            <p>Assists: {lastMatchStats.assists}</p>
            <p>Distance run: {lastMatchStats.distance}</p>
            {/* etc. */}
          </div>
          <div className="text-xl">Overall: {lastMatchStats.overall} ⭐</div>
        </div>

        <div className="bg-white text-black p-4 rounded">
          <h2 className="text-xl font-bold mb-2">Next week schedule</h2>
          <div className="flex justify-around">
            <div className="text-center">
              <p>Monday</p>
              <p>Training session 9:00-12:00</p>
            </div>
            <div className="text-center">
              <p>Tuesday</p>
              <p>Training session 9:00-12:00</p>
            </div>
            <div className="text-center">
              <p>Wednesday</p>
              <p>Day off</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
