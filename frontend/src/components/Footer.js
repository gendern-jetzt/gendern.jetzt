import React from "react";
import "./Footer.css";

class Footer extends React.Component {
  render() {
    return (
      <div className="footer">
        <div className="container">
          <footer>
            <div>
              <p>
                © Karl Engelhardt, Charlotte Friedrich, Felix Haak & Philipp
                Müller GbR
              </p>
            </div>
            <div>
              <div>
                <ul>
                  <li>
                    <a href="/impressum">
                      Impressum
                    </a>
                  </li>
                  <li>
                    <a href="/contact">
                      Kontakt
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </footer>
        </div>
      </div>
    );
  }
}

export default Footer;
