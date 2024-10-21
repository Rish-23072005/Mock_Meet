import React from "react";
import {Link} from "react-router-dom"
import Navbar from "../components/navbar.component";
import Footer from "../components/footer.component";

import SideBot from "../assets/images/sideBot.svg"

import axios from "axios";
// import { useNavigate } from "react-router-dom";

const Audio= ()=>{
    // const navigate = useNavigate();

    const handleResultClick = async () => {
        try {
          // Show a pop-up message to inform the user
          alert("Emotion Analysis soon");
      
          // Call the Flask endpoint to prepare the audio dashboard data
          await axios.post("http://localhost:5000/prep_audiodash");
      
          // Navigate to the backend dashboard
          window.location.href = "http://localhost:5000/prep_audiodash";
        } catch (error) {
          console.error("Error preparing audio dashboard:", error);
        }
      };
      
    return (
        <>
        <Navbar/>
            <div className="my-16">
                <div className="d-flex  mb-16">
                    <div className="w-full p-10 m-16 " style={{ margin:"150px 100px 220px 220px "}} >
                        <h1 className="display-2  font-link "style={{fontWeight:"bolder", marginBottom:"60px"}}>audio interview.</h1>
                       
                        <div className="fs-4 mb-16" style={{width:"60%"}}>
                            <p>Use the audio interview simulator  and get a feedback on how our 
                                algorithm interprets your facial emotions compared to other candidates.
                            </p>
                            <br />
                            <p className="" style={{fontWeight:"lighter"}}>
                                You will be provided a feedback on your facial emotions such as 
                            </p>
                            <br />
                            <p style={{fontWeight:"lighter"}}>Anger | Happiness | Fear | Sadness | Surprise | Disgust</p>
                        </div>
                        <br />
                        <br />

                        {/* <div className="d-flex gap-10">
                            <Link to="/interview/a">
                            <button className="bg-black font-light px-5 py-2 rounded-2">Interview</button>
                            </Link>
                            <button classNa
                            me="border-2 border-black font-dark px-6 py-2 rounded-2">Result</button>
                        </div> */}

                        <div className=" gap-2" >

                            <Link to="/interview/a" >
                                <button type="button" class="btn btn-dark px-3 mr-4 py-2" style={{margin:"20px"}}>Interview</button>
                            </Link>
                            <button
      type="button"
      className="btn btn-outline-dark py-2"
      onClick={handleResultClick}
    >
      Result
    </button>

                        </div>

                    </div>
                    
                    <div >
                        <div class="sideBot-img"  className="w-96 h-full">
                            <img src={SideBot} className="h-full w-full " alt="Side Bot" />
                        </div>
                    </div>
                </div>
            </div>
            <Footer/>
        </>
    );
}

export default Audio;