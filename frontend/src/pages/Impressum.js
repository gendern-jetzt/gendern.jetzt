import React from "react";
import "./Impressum.css";

class Impressum extends React.Component {
  render() {
    return (
      <div className="content">
        <div className="containe center">
          <h1>Impressum</h1>
          <div className="name contact">
            <h3>Genderly*</h3>
            <p>kontakt@genderly.eu</p>
          </div>
          <div className="address contact">
            <h3>Adresse</h3>
              <ul>
                <li>Engelhardt, Friedrich, Haak, Müller GbR</li>
                <li>Droysenstraße 19</li>
                <li>10629 Berlin</li>
                <li>Steuer-Nummer: 13/449/04359</li>
              </ul>
          </div>
        </div>
      </div>
    );
  }
}

export default Impressum;
