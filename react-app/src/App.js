import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login/Login";
import CoachDashboard from "./pages/CoachDashboard/CoachDashboard";
import PlayerDashboard from "./pages/PlayerDashboard/PlayerDashboard";
import LeagueNews from "./pages/LeagueNews/LeagueNews";
// etc...

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/coach-dashboard" element={<CoachDashboard />} />
      <Route path="/player-dashboard" element={<PlayerDashboard />} />
      <Route path="/league-news" element={<LeagueNews />} />
    </Routes>
  );
}
