import { Link } from "react-router-dom";
import milanLogo from '../assets/milan.png'; 

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between p-4 bg-gray-800 text-white">
      <div className="flex items-center">
        <img src={milanLogo} alt="AC Milan" className="h-10 w-auto" />
        <span className="ml-2 text-xl font-bold">DASHBOARD</span>
      </div>
      <ul className="flex gap-4">
        <li>
          <Link to="/players">Players</Link>
        </li>
        <li>
          <Link to="/plan-training">Plan Training</Link>
        </li>
        <li>
          <button
            onClick={async () => {
              try {
                const res = await fetch("http://localhost:8000/logout/", {
                  method: "POST",
                  credentials: "include",  // if you're using session cookies
                });
                if (!res.ok) throw new Error("Failed to logout");
                // After logging out, redirect or do something
                window.location.href = "/";
              } catch (err) {
                alert(err.message);
              }
            }}
          >
            Logout
          </button>
        </li>
      </ul>
    </nav>
  );
}
