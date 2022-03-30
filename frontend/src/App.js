import './App.css';
import React from "react"
import Footer from "./components/Footer.js"
import Navbar from "./components/Navbar.js"
import About from './pages/About';
import Home from './pages/Home';
import Faq from './pages/Faq';
import Contact from './pages/Contact';
import Support from './pages/Support';
import Privacy from './pages/Privacy';
import Impressum from './pages/Impressum';
import Gendern from './pages/Gendern';

import {
  Switch,
  BrowserRouter as Router,
  Route
} from 'react-router-dom'

class App extends React.Component {
  render () {
    return (
      <div className="App">
        <Router>
          <Navbar />
          <Switch>
            <Route path="/" exact component={Home}></Route>
            <Route path="/about" component={About}></Route>
            <Route path="/faq" component={Faq}></Route>
            <Route path="/contact" component={Contact}></Route>
            <Route path="/support" component={Support}></Route>
            <Route path="/privacy" component={Privacy}></Route>
            <Route path="/impressum" component={Impressum}></Route>
            <Route path="/gendern" component={Gendern}></Route>
          </Switch>
        </Router>
        <Footer />
      </div>
    )
  }
}

export default App;
