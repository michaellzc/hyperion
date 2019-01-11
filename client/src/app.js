import React, { Component } from 'react';
import { Provider } from 'unstated';
import { Router, Link } from '@reach/router';
import PrivateRoute from './components/private-route';
// import ErrorBoundary from './components/error-boundary';
import HomePage from './pages/home-page';
import LoginPage from './pages/login-page';

function Dashboard() {
  return (
    <div>
      Protected dashboard <Link to="/">Go to home page</Link>
    </div>
  );
}

class App extends Component {
  render() {
    return (
      <Provider>
        <Router>
          <HomePage path="/" />
          <LoginPage path="login" />
          <PrivateRoute as={Dashboard} path="/dashboard" />
        </Router>
      </Provider>
    );
  }
}

export default App;
