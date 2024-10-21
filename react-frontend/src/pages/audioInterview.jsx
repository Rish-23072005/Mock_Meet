import React, { useState } from "react";
import axios from 'axios';
import Navbar from "../components/navbar.component";
import Footer from "../components/footer.component";
import AudioRecorder from "../components/audiorecorder"; // Adjust import path as needed
import './sidebar.css'; // Assuming you have CSS for sidebar styles
import Frontend from "../assets/images/frontend.jpg";
import Backend from "../assets/images/backend.png";
import FullStack from "../assets/images/fullStack.jpg";

const techPositions = [
  { id: 1, title: "Frontend Developer", image: Frontend },
  { id: 2, title: "Backend Developer", image: Backend },
  { id: 3, title: "Full Stack Developer", image: FullStack },
];

const AudioInterview = () => {
  const [isRecording, setIsRecording] = useState(false);
  // const [audioUrl, setAudioUrl] = useState(null);
  // const [audioBlob, setAudioBlob] = useState(null);
  const [showSidebar, setShowSidebar] = useState(false);
  const [questions, setQuestions] = useState([]);
  // const mediaRecorderRef = useRef(null);
  // const streamRef = useRef(null);

  // const startRecording = async () => {
  //   try {
  //     const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  //     streamRef.current = stream;
  
  //     const options = { mimeType: "audio/webm" };
  //     const mediaRecorder = new MediaRecorder(stream, options);
  
  //     mediaRecorder.ondataavailable = handleDataAvailable;
  //     mediaRecorder.start();
  //     mediaRecorderRef.current = mediaRecorder;
  
  //     setIsRecording(true);
  //     setShowSidebar(true); // Show sidebar when recording starts
  //   } catch (error) {
  //     console.error("Error starting audio recording: ", error);
  //   }
  // };
  const startRecording = async () => {
    try {
      setIsRecording(true);
      setShowSidebar(true); // Show sidebar when recording starts

      // Call the Flask endpoint to start the audio recording
      const response = await axios.post('http://localhost:5000/prep_recording');
      console.log(response.data.message);
    } catch (error) {
      console.error('Error starting audio recording:', error);
      setIsRecording(false);
      setShowSidebar(false); // Hide sidebar in case of an error
    }
  };
  
  // const stopRecording = () => {
  //   if (mediaRecorderRef.current) {
  //     mediaRecorderRef.current.stop();
  //     if (streamRef.current) {
  //       streamRef.current.getTracks().forEach((track) => track.stop());
  //     }
  //   }
  //   setIsRecording(false);
  //   setShowSidebar(false); // Hide sidebar when recording stops
  //   uploadAudio();
  // };

  const stopRecording = () => {
    // Since the recording is happening on the backend, there's no need to explicitly stop it from React
    setIsRecording(false);
    setShowSidebar(false);
  };
  

//   const handleDataAvailable = (event) => {
//   console.log('Event:', event);
//   if (event.data && event.data.size > 0) {
//     const audioBlob = new Blob([event.data], { type: "audio/webm" });
//     const audioUrl = URL.createObjectURL(audioBlob);
//     setAudioBlob(audioBlob);
//     setAudioUrl(audioUrl);
//   } else {
//     console.error('Data is undefined or has no size');
//   }
// };


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
      startRecording();  // Start recording after questions are fetched
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  // const uploadAudio = async () => {
  //   if (audioBlob) {
  //     const formData = new FormData();
  //     formData.append('audio', audioBlob, 'recorded-audio.webm');

  //     try {
  //       const response = await axios.post('http://localhost:5000/upload-audio', formData, {
  //         headers: {
  //           'Content-Type': 'multipart/form-data'
  //         }
  //       });
  //       console.log('Emotion detected:', response.data.emotion);
  //       // Handle emotion state update or other actions as needed
  //     } catch (error) {
  //       console.error('Error uploading audio:', error);
  //     }
  //   }
  // };

  return (
    <>
      <Navbar />
      <div className="d-flex flex-column align-items-center my-2 px-52 ">
        <h1 className="display-2 font-link font-weight-bold " style={{ fontWeight: "bolder" }}>
          Audio Interview
        </h1>

        <div className="w-full h-full d-flex " style={{ gap: 80 }}>
          <div className="w-full h-full " style={{ marginLeft: "75px" }}>

            <div className="app">
              <div className="app__container bg-dark p-2" style={{ height: "500px", width: "700px", marginBottom: "60px", marginLeft: "-50px" }}>
                <div style={{ marginTop: "190px", marginLeft: "20px" }}>
                  <AudioRecorder
                    onStartRecording={() => setShowSidebar(true)}
                    onStopRecording={stopRecording}
                    // onAudioRecorded={handleDataAvailable}
                  />
                </div>
              </div>
            </div>

            <div className="d-flex m-4 justify-evenly ">
              {isRecording ? (
                <button
                  className="border-2 m-4 text-white bg-blue-900 px-8 py-2 border-blue fs-2 font-medium rounded-2"
                  onClick={stopRecording}
                >
                  Stop Audio
                </button>
              ) : (
                <button
                  className="border-2 m-4 text-white bg-blue-900 px-8 py-2 border-blue fs-2 font-medium rounded-2"
                  onClick={startRecording}
                >
                  Start Audio
                </button>
              )}
            </div>

          </div>

          <div className="d-flex flex-column ml-12 text-xl font-regular" style={{ marginTop: "25px", gap: 10, height: "100%" }}>
            <div className="w-full rounded-2 fs-4 p-2 ml-4" style={{ backgroundColor: "lightgrey", height: "100px", width: "380px" }}>
              You will have 15 mins to answer the questions mentioned above.
            </div>
            <div className="rounded-2 p-4 fs-4" style={{ backgroundColor: "lightgrey", height: "370px", width: "380px" }}>
              {questions.map((question, index) => (
                <div key={index}>
                  {question}
                  <br />
                </div>
              ))}
            </div>
            <div className="d-flex justify-evenly pt-5 ">
              <button className="border-2 px-3 text-blue border-black fs-4 font-medium rounded-2">
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
              <div key={position.id} className="position" onClick={() => { handlePositionSelect(position.title); setShowSidebar(false); }}>
                <img src={position.image} alt={position.title} style={{ width: "50px", height: "50px" }} />
                <span>{position.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      {/* {audioUrl && (
        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <h3>Recorded Audio:</h3>
          <audio controls>
            <source src={audioUrl} type="audio/webm" />
            Your browser does not support the audio element.
          </audio>
          <br />
          <a href={audioUrl} download="recorded-audio.webm">
            <button className="btn btn-primary">Download Audio</button>
          </a>
        </div>
      )} */}
      <Footer />
    </>
  );
};

export default AudioInterview;
