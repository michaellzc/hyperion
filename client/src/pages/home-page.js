import React, { Component } from 'react';
import { Link } from '@reach/router';
import logo from '../assets/logo.svg';
import './app.css';

class HomePage extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <Link to="dashboard" className="App-link">
            Dashboard (Auth required)
          </Link>
        </header>
      </div>
    );
  }
}

export default HomePage;
