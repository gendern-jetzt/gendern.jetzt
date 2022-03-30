import React from "react";

function Mailto({ email, subject, body, ...props }) {
  return (
    <a href={`mailto:${email}?subject=${subject || ""}&body=${body || ""}`}>
      {props.children}
    </a>
  );
}

class Contact extends React.Component {
  render() {
    return (
      <div className="content">
        <div className="container center">
          <h2>Für Anfragen, schicke uns eine Mail 📬 an:</h2>
          <Mailto email="kontakt@genderly.eu" subject="Anfrage">
            kontakt@genderly.eu
          </Mailto>
        </div>
      </div>
    );
  }
}

export default Contact;
