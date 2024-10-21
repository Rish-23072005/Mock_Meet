import React from "react";
import { FaUserCircle } from "react-icons/fa";
import { Link } from "react-router-dom";

import Logo from "../assets/logo/logo.webp";

const Newnavbar = () => {
  return (
    <div style={{ backgroundColor: "#f8f9fa", height: "70px", boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)" }}>
      <nav className="container d-flex align-items-center justify-content-between py-2">
        <Link to="/">
          <img src={Logo} alt="logo" style={{ height: "80px" }} />
        </Link>
        <div className="d-flex align-items-center">
          <Link to="/create-interview">
            <button className="btn btn-outline-primary mx-2">Create Interview</button>
          </Link>
          <Link to="/profile">
            <FaUserCircle className="fs-1 text-primary" />
          </Link>
        </div>
      </nav>
    </div>
  );
};

export default Newnavbar;
