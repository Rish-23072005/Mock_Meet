import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Landing from "../src/pages/landing.pages";
import Audio from "./pages/audio";
import Video from "./pages/video";
import VideoInterview from "./pages/videoInterview";
import AudioInterview from "./pages/audioInterview";
import Login from "./pages/login";
import AppDashboard from "./pages/AppDashboard";
// import CreateInterview from "./pages/CreateInterview"; // Import CreateInterview component
// import Interview from "./pages/Interview";
import CreateInterview from "./pages/CreateInterview";
import PastInterview from "./pages/PastInterviews";
import UpcomingInterview from "./pages/UpcommingInterviews";

import Interviewers from './pages/Interviewrs';
import Questions from './pages/Questions';
import Settings from './pages/Settings';
import Reports from './pages/Reports';

import Dashboard from './pages/Dashboard';


const App = () => {
  return (
    <div>
      <Router>
        <div>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/audio" element={<Audio />} />
            <Route path="/video" element={<Video />} />
            <Route path="/interview/v" element={<VideoInterview />} />
            <Route path="/interview/a" element={<AudioInterview />} />
            <Route path="/profile" element={<AppDashboard />} />
            <Route path="/create-interview" element={<CreateInterview />} />
            <Route path="/past-interviews" element={<PastInterview />} />
            <Route path="/upcoming-interviews" element={<UpcomingInterview />} />
            <Route path="/interviewers" element={<Interviewers />} />
            
            <Route path="/interview-questions" element={<Questions />} />
            <Route path="/interview-reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/dashboard" element={<Dashboard />} />
            


          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
