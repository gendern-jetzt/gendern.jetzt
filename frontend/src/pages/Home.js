import React from "react";
import "./Home.css";
import EditorContainer from "../components/EditorContainer";

class Home extends React.Component {
  render() {
    return (
      <div className="content">
        <div className="container">
          <div className="welcome-container">
            <h1 class="center">Gendern ganz einfach</h1>
            <p class="center">Genderly macht gendergerechtes Schreiben ganz einfach - mit Machine Learning.<br></br>
            Probiere es jetzt aus ⬇️</p>
          </div>
          <EditorContainer />
          <div className="supported-by center">
            <h2>Förderungen</h2>
            <div className="supported-by-logos center">
              <div className="img-container">
                <a href={"https://www.bmbf.de/"} target="_blank" rel="noopener noreferrer">
                  <img src="/bmbf_logo.jpg" alt="Logo des BMBF" width="300" height="200"/>
                </a>
              </div>
              <div className="img-container">
                <a href={"https://prototypefund.de/"} target="_blank" rel="noopener noreferrer">
                  <img src="/PrototypeFund_Logo.svg" alt="Logo des Prototype" width="250" height="200"/>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
