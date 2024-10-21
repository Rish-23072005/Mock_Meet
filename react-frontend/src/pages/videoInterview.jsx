import React, { useState } from "react";
import Navbar from "../components/navbar.component";
import Footer from "../components/footer.component";
import "./sidebar.css";
import Frontend from "../assets/images/frontend.jpg";
import Backend from "../assets/images/backend.png";
import FullStack from "../assets/images/fullStack.jpg";

const techPositions = [
  { id: 1, title: "Frontend Developer", image: Frontend },
  { id: 2, title: "Backend Developer", image: Backend },
  { id: 3, title: "Full Stack Developer", image: FullStack },
];

const VideoInterview = () => {
  const [isRecording, setIsRecording] = useState(false);
  // const [videoUrl, setVideoUrl] = useState(null);
  const [showSidebar, setShowSidebar] = useState(false);
  const [questions, setQuestions] = useState([]);

  const handlePositionSelect = async (position) => {
    try {
      console.log('Selected position:', position);
      const response = await fetch('http://localhost:5000/get-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ position }),
      });
      const data = await response.json();
      console.log('Received questions:', data);
      setQuestions(data);
      setIsRecording(true);  // Optional: Start recording after questions are fetched
      setShowSidebar(false);
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  const handleStartClick = () => {
    setShowSidebar(true);
  };

  return (
    <>
      <Navbar />
      <div className="d-flex flex-column align-items-center px-52 " style={{ marginBottom: "30px" }}>
        <h1 className="display-2 font-link font-weight-bold mb-16" style={{ fontWeight: "bolder", marginTop: "20px", marginBottom: "15px" }}>
          Video Interview
        </h1>

        <div className="w-full h-full d-flex " style={{ gap: 120 }}>
          <div className="w-full h-full" style={{ marginLeft: "100px" }}>
            <div className="app">
              <div className="app__container bg-dark p-2" style={{ height: "440px", width: "600px", marginBottom: "20px" }}>
                {isRecording ? (
                  <img
                    src="http://localhost:5000/video_feed"
                    alt="Video Feed"
                    style={{ height: "100%", width: "100%" }}
                  />
                ) : (
                  <div style={{ height: "100%", width: "100%", color: "white", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    Video Feed will appear here
                  </div>
                )}
              </div>
              <div className="app__input">
                {isRecording ? (
                  <button
                    className="border-2 px-3 text-blue border-black fs-4 font-medium rounded-2"
                    onClick={() => setIsRecording(false)}
                    style={{ marginTop: "20px", marginBottom: "20px" }}
                  >
                    Stop Recording
                  </button>
                ) : (
                  <button
                    className="border-2 px-3 text-blue border-black fs-4 font-medium rounded-2"
                    onClick={handleStartClick}
                    style={{ marginTop: "20px", marginBottom: "20px" }}
                  >
                    Start Recording
                  </button>
                )}
              </div>
            </div>
          </div>

          <div className="d-flex flex-column gap-4 ml-12 text-xl font-regular" style={{ marginTop: "30px", height: "100%" }}>
            <div className="w-full rounded-2 fs-4 p-2 ml-4" style={{ backgroundColor: "lightgrey", height: "100px", width: "380px" }}>
              You will have 15 mins to answer the questions mentioned above.
            </div>
            <div className="rounded-2 p-4 fs-4" style={{ backgroundColor: "lightgrey", height: "310px", width: "380px" }}>
              {questions.map((question, index) => (
                <div key={index}>
                  {question}
                  <br />
                </div>
              ))}
            </div>
            <div className="d-flex justify-evenly mb-10 pt-5">
              <button className="border-2 px-3 text-blue border-black fs-4 font-medium rounded-2" style={{ marginTop: "-25px" }}>
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>

      {showSidebar && (
        <div className="sidebar">
          <h2>Select a Position</h2>
          <div className="positions">
            {techPositions.map((position) => (
              <div key={position.id} className="position" onClick={() => handlePositionSelect(position.title)}>
                <img src={position.image} alt={position.title} style={{ width: "50px", height: "50px" }} />
                <span>{position.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <Footer />
    </>
  );
};

export default VideoInterview;
