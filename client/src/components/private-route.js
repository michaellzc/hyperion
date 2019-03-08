import React, { Component } from 'react';
import { navigate } from '@reach/router';
import Login from '../pages/login-page';
import { AuthStore } from '../stores';
import { inject } from '../utils';

// https://gist.github.com/ryanflorence/eba97731b5579a1c01702c9d394b3feb
class PrivateRoute extends Component {
  async componentDidMount() {
    let [authStore] = this.props.stores;
    try {
      let user = await authStore.getUserInfo();
      if (user.hasOwnerProperty('isActive') && user.isActive) {
        await navigate('/inactive');
      }
    } catch (error) {
      if (error.response && error.response.status !== 200) {
        await navigate(`/login?from=${window.location.pathname}`);
      }
    }
  }

  render() {
    let { as: Comp, ...props } = this.props;
    let [authStore] = this.props.stores;
    return authStore.user ? <Comp {...props} /> : <Login />;
  }
}

export default inject([AuthStore])(PrivateRoute);
