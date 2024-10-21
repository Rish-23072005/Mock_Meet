import React from 'react';
import Navbar from "../components/navbar.component";

const CreateInterview = () => {
  const containerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #f5f7fa, #c3cfe2)',
    fontFamily: 'Arial, sans-serif',
    textAlign: 'center'
  };

  const contentStyle = {
    background: 'white',
    padding: '50px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)'
  };

  const titleStyle = {
    fontSize: '3em',
    color: '#333',
    marginBottom: '20px'
  };

  const textStyle = {
    fontSize: '1.2em',
    color: '#666',
    marginBottom: '40px'
  };

  const loaderStyle = {
    border: '5px solid #f3f3f3',
    borderTop: '5px solid #3498db',
    borderRadius: '50%',
    width: '50px',
    height: '50px',
    animation: 'spin 2s linear infinite'
  };

  const keyframes = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;

  return (
    <>
      <Navbar />
      <div style={containerStyle}>
        <style>{keyframes}</style>
        <div style={contentStyle}>
          <h1 style={titleStyle}>Coming Soon</h1>
          <p style={textStyle}>Our new feature is on the way. Stay tuned!</p>
          <div style={loaderStyle}></div>
        </div>
      </div>
    </>
  );
};

export default CreateInterview;
