import React from "react";
import { FaUserCircle } from "react-icons/fa";
import { Link } from "react-router-dom";
// import axios from "axios";  // Import axios for making the API request
import Logo from "../assets/logo/logo.webp";

const Navbar = () => {
  // const navigate = useNavigate();  // useNavigate hook for programmatic navigation

  const handleCreateInterview = () => {
    // Directly navigate to the backend route
    window.location.href = "http://localhost:5000/mockmeet";
  };
  

  return (
    <div style={{ backgroundColor: "#f8f9fa", height: "70px", boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)" }}>
      <nav className="container d-flex align-items-center justify-content-between py-2">
        <Link to="/">
          <img src={Logo} alt="logo" style={{ height: "80px" }} />
        </Link>
        <div className="d-flex align-items-center">
          <div className="d-flex gap-4" style={{ marginRight: "20px" }}>
            <Link to="/video">
              <button type="button" className="btn btn-outline-dark py-2">Video</button>
            </Link>
            <Link to="/audio">
              <button type="button" className="btn btn-outline-dark py-2">Audio</button>
            </Link>
          </div>
          <button className="btn btn-outline-primary mx-2" onClick={handleCreateInterview}>
            Live Mockmeet
          </button>
          <Link to="/profile">
            <FaUserCircle className="fs-1 text-primary" />
          </Link>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
