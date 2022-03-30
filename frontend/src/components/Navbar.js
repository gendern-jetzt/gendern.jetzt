import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  return (
    <>
      <div className="nav-bar">
        <nav>
          <ul className="menu">
            <li className="logo">
              <NavLink exact to="/">
                <img src="logo.svg" alt="Genderly logo"></img>
              </NavLink>
            </li>
            <li>
              <NavLink exact activeClassName="active" to="/">
                Home
              </NavLink>
            </li>
            <li>
              <NavLink exact activeClassName="active" to="/about">
                Über uns
              </NavLink>
            </li>
            <li>
              <NavLink exact activeClassName="active" to="/faq">
                FAQ
              </NavLink>
            </li>
            <li>
              <NavLink exact activeClassName="active" to="/gendern">
                Alles übers Gendern
              </NavLink>
            </li>
            <li>
              <NavLink exact activeClassName="active" to="/contact">
                Kontakt
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
};

export default Navbar;
