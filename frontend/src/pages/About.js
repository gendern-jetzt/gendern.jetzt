import React from "react";
import "./About.css";

class About extends React.Component {
  render() {
    return (
      <>
        <div className="content">
          <div className="container">
            <h1>Hi!</h1>
            <p>
              Wir sind Karl, Charlotte, Felix und Philipp- das Team hinter
              Genderly. Kennengelernt haben wir uns in einem interdisziplinären
              Seminar an der Humboldt- Universität. Für die technische Umsetzung
              sind vor allem unsere beiden Informatikstudenten Karl und Felix
              verantwortlich. Der linguistische Input stammt von Charlotte (im
              BA germanistische Linguistik) und Philipp (MA Linguistik). Mit
              unseren unterschiedlichen Kompetenzen ergänzen wir uns gegenseitig
              und die Zuständigkeiten sind fließend.
            </p>
            <p>
              Wir möchten Genderly stetig verbessern. Dafür sind wir auch auf
              deine Hilfe angewiesen. Wenn dir bei der Nutzung technische Fehler
              oder Begriffe, die noch nicht erkannt werden auffallen, melde dich
              bei <a href="mailto:kontakt@genderly.eu">kontakt@genderly.eu</a>.
              In unserer Arbeit legen wir Wert darauf, niemanden auszuschließen.
              Wenn dir also etwas auffällt, wie wir Genderly inklusiver
              gestalten können, lass es uns unbedingt wissen!
            </p>
            <p>
              Genderly wird unterstützt durch die HU Berlin - Lehrstuhl
              Maschinelles Lernen, den Prototype Fund und die Humboldt
              Universitäts- Gesellschaft Außerdem danken wir unseren unzähligen
              Text- Spender*innen.
            </p>
          </div>
        </div>
      </>
    );
  }
}

export default About;
