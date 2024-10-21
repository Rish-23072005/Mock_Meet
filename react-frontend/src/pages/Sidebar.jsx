import React from 'react';
import { BsGrid1X2Fill, BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsListCheck, BsMenuButtonWideFill, BsFillGearFill } from 'react-icons/bs';
import { IoIosMicrophone } from "react-icons/io";
import { Link } from 'react-router-dom';

function Sidebar({ openSidebarToggle, OpenSidebar }) {
  return (
    <aside id="sidebar" className={openSidebarToggle ? "sidebar-responsive" : ""}>
      <div className='sidebar-title'>
        <div className='sidebar-brand'>
          <IoIosMicrophone className='icon_header' />
          <span>MOCKMATE</span>
          <img src="https://plus.unsplash.com/premium_photo-1689977871600-e755257fb5f8?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Profile" className="profile-picture" />
        </div>
        <span className='icon close_icon' onClick={OpenSidebar}>X</span>
      </div>

      <ul className='sidebar-list'>
        <li className='sidebar-list-item'>
          <Link to="/dashboard">
            <BsGrid1X2Fill className='icon' /> Dashboard
          </Link>
        </li>
        <li className='sidebar-list-item'>
          <Link to="/past-interviews">
            <BsFillArchiveFill className='icon' /> Past Interviews
          </Link>
        </li>
        <li className='sidebar-list-item'>
          <Link to="/upcoming-interviews">
            <BsFillGrid3X3GapFill className='icon' /> Upcoming Interviews
          </Link>
        </li>
        <li className='sidebar-list-item'>
          <Link to="/interviewers">
            <BsPeopleFill className='icon' /> Interviewers
          </Link>
        </li>
        <li className='sidebar-list-item'>
          <Link to="/interview-questions">
            <BsListCheck className='icon' /> Interview Questions
          </Link>
        </li>
        <li className='sidebar-list-item'>
          <Link to="/interview-reports">
            <BsMenuButtonWideFill className='icon' /> Interview Reports
          </Link>
        </li>
        <li className='sidebar-list-item'>
          <Link to="/settings">
            <BsFillGearFill className='icon' /> Settings
          </Link>
        </li>
      </ul>
    </aside>
  );
}

export default Sidebar;
