import React from "react";
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin, FaGithub, FaDiscord } from "react-icons/fa";
import { MdOutlineCopyright } from "react-icons/md";
import { MDBFooter, MDBContainer, MDBRow, MDBCol, MDBIcon } from 'mdb-react-ui-kit';

const Footer = () => {
  return (
    <MDBFooter className='bg-dark text-white text-center text-lg-start'>
      <MDBContainer className='p-4'>
        <MDBRow>
          <MDBCol lg='6' md='12' className='mb-4 mb-md-0'>
            <h5 className='text-uppercase'>Mockmate AI Interviews</h5>
            <p>
              Simplifying your interview preparations with AI-driven mock interviews. Connect with us on social media or reach out via the contact information below.
            </p>
          </MDBCol>

          <MDBCol lg='3' md='6' className='mb-4 mb-md-0'>
            <h5 className='text-uppercase'>Social Media</h5>
            <div className='d-flex justify-content-center justify-content-md-start'>
              <a href='https://facebook.com' className='text-white m-2' target="_blank" rel="noopener noreferrer"><FaFacebook size={30} /></a>
              <a href='https://twitter.com' className='text-white m-2' target="_blank" rel="noopener noreferrer"><FaTwitter size={30} /></a>
              <a href='https://instagram.com' className='text-white m-2' target="_blank" rel="noopener noreferrer"><FaInstagram size={30} /></a>
              <a href='https://linkedin.com' className='text-white m-2' target="_blank" rel="noopener noreferrer"><FaLinkedin size={30} /></a>
            </div>
          </MDBCol>

          <MDBCol lg='3' md='6' className='mb-4 mb-md-0'>
            <h5 className='text-uppercase'>Useful Links</h5>
            <ul className='list-unstyled'>
              <li className='mb-2'>
                <a href='https://github.com/' className='text-white' target="_blank" rel="noopener noreferrer"><FaGithub className='me-2' />GitHub Repository</a>
              </li>
              <li className='mb-2'>
                <a href='https://discord.com/' className='text-white' target="_blank" rel="noopener noreferrer"><FaDiscord className='me-2' />Join Our Discord</a>
              </li>
              <li className='mb-2'>
                <a href='https://github.com/' className='text-white' target="_blank" rel="noopener noreferrer"><MDBIcon icon='file-alt' className='me-2' />Code of Conduct</a>
              </li>
            </ul>
          </MDBCol>
        </MDBRow>
      </MDBContainer>

      <div className='text-center p-3' style={{ backgroundColor: 'rgba(0, 0, 0, 0.2)' }}>
        <MDBRow>
          <MDBCol className='d-flex justify-content-center align-items-center'>
            <MdOutlineCopyright className="fs-2 me-2" />
            2024 MockMate AI Interviews. All rights reserved.
          </MDBCol>
        </MDBRow>
      </div>
    </MDBFooter>
  );
};

export default Footer;
