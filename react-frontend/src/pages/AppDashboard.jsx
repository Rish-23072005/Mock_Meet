import { useState } from 'react'
import './App.css'
import Header from './Header'
import Sidebar from './Sidebar'
import Home from './Home'

// import PastInterview from './PastInterviews';

// import UpcomingInterview from './UpcommingInterviews';

function App() {
  

  return (
    <div className="grid-container">
      <Header/>
      <Sidebar/>
      <Home/>
      {/* <PastInterview/>
      <UpcomingInterview/> */}

    </div>
  )
}

export default App
