import React from 'react';
    import { NavLink } from 'react-router-dom';
    import { AiFillHome, AiFillRobot, AiFillBook, AiFillPieChart } from 'react-icons/ai';
    import './Sidebar.css';

    function Sidebar() {
      return (
        <div className="sidebar">
          <div className="sidebar-header">
            <h2>Peak</h2>
          </div>
          <nav>
            <NavLink to="/" exact activeClassName="active">
              <AiFillHome /> Home
            </NavLink>
            <NavLink to="/portfolio" activeClassName="active">
              <AiFillPieChart /> Portfolio
            </NavLink>
            <NavLink to="/ai-assistant" activeClassName="active">
              <AiFillRobot /> PeakAI
            </NavLink>
            <NavLink to="/learning" activeClassName="active">
              <AiFillBook /> Learn
            </NavLink>
          </nav>
        </div>
      );
    }

    export default Sidebar;
