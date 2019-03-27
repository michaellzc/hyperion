import React, { Component } from 'react';
import UNSTATED from 'unstated-debug';
import { Provider } from 'unstated';
import { Router } from '@reach/router';
import { createGlobalStyle } from 'styled-components/macro';
import PrivateRoute from './components/private-route';
// import ErrorBoundary from './components/error-boundary';
import HomePage from './pages/home-page';
import LoginPage from './pages/login-page';
import SignupPage from './pages/signup-page';
import InactivePage from './pages/inactive-page';
import NotFoundPage from './pages/not-found-page';
import UserProfilePage from './pages/user-profile-page';

if (process.env.NODE_ENV === 'development') {
  UNSTATED.logStateChanges = true;
} else {
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
          <PrivateRoute as={HomePage} path="posts/:postId" />
          <LoginPage path="login" />
          <SignupPage path="signup" />
          <InactivePage path="inactive" />
          <PrivateRoute as={UserProfilePage} path=":authorId" />
          <NotFoundPage default />
        </Router>
      </Provider>
    );
  }
}

export default App;
