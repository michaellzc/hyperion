import React, { Component } from 'react';
import UNSTATED from 'unstated-debug';
import { Provider } from 'unstated';
import { Router } from '@reach/router';
import { createGlobalStyle } from 'styled-components/macro';
import PrivateRoute from './components/private-route';
// import ErrorBoundary from './components/error-boundary';
import HomePage from './pages/home-page';
import LoginPage from './pages/login-page';

if (process.env.NODE_ENV === 'development') {
  UNSTATED.logStateChanges = false;
}

let GlobalStyle = createGlobalStyle`
  .ant-layout {
      overflow-x: hidden;
  }
`;

class App extends Component {
  render() {
    return (
      <Provider>
        <GlobalStyle />
        <Router>
          <PrivateRoute as={HomePage} path="/" />
          <LoginPage path="login" />
        </Router>
      </Provider>
    );
  }
}

export default App;
