// VideoChat.js
import React, { useState, useEffect } from 'react';
import './VideoChat.module.css'; // Don't forget to import the CSS file!


const Interview = () => {
  const [localVideo, setLocalVideo] = useState(null);
  const [remoteVideo, setRemoteVideo] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    // Initialize video elements
    const localVideoElement = document.getElementById('local-video');
    const remoteVideoElement = document.getElementById('remote-video');
    setLocalVideo(localVideoElement);
    setRemoteVideo(remoteVideoElement);
  }, []);

  const handleSendMessage = () => {
    // Send message to chat
    setChatMessages([...chatMessages, newMessage]);
    setNewMessage('');
  };

  const handleVideoStart = () => {
    // Start video
  };

  const handleVideoStop = () => {
    // Stop video
  };

  const handleMuteMic = () => {
    // Mute mic
  };

  const handleUnmuteMic = () => {
    // Unmute mic
  };

  const handleShareScreen = () => {
    // Share screen
  };

  const handleStopScreenShare = () => {
    // Stop screen share
  };

  return (
    <div className="container">
      <div className="video-container">
        <div className="local-video">
          <video id="local-video" width="100%" height="100%"></video>
        </div>
        <div className="remote-video">
          <video id="remote-video" width="100%" height="100%"></video>
        </div>
      </div>
      <div className="chat-container">
        <div className="chat-header">
          <h2>Chat</h2>
        </div>
        <div className="chat-messages">
          <ul id="chat-messages-list">
            {chatMessages.map((message, index) => (
              <li key={index}>{message}</li>
            ))}
          </ul>
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type a message..."
            className="chat-input-field" // Add class name
          />
          <button onClick={handleSendMessage} className="send-chat-message-btn">Send</button> 
        </div>
      </div>
      <div className="controls-container">
        <button onClick={handleVideoStart} className="control-btn">Start Video</button>
        <button onClick={handleVideoStop} className="control-btn">Stop Video</button>
        <button onClick={handleMuteMic} className="control-btn">Mute Mic</button>
        <button onClick={handleUnmuteMic} className="control-btn">Unmute Mic</button>
        <button onClick={handleShareScreen} className="control-btn">Share Screen</button>
        <button onClick={handleStopScreenShare} className="control-btn">Stop Screen Share</button>
      </div>
    </div>
  );
};

export default Interview;