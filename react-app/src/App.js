import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login/Login";
import CoachDashboard from "./pages/CoachDashboard/CoachDashboard";
import PlayerDashboard from "./pages/PlayerDashboard/PlayerDashboard";
import ChangePassword from "./pages/ChangePassword/ChangePassword";
import ReportInjury from "./pages/ReportInjury/ReportInjury";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/coach-dashboard" element={<CoachDashboard />} />
      <Route path="/player-dashboard" element={<PlayerDashboard />} />
      <Route path="/change-password" element={<ChangePassword />} />
      <Route path="/report-injury" element={<ReportInjury />} />
    </Routes>
  );
}
