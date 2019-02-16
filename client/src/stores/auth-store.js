import { Container } from 'unstated';
import * as API from '../api';

class AuthStore extends Container {
  state = {
    user: null,
  };

  get user() {
    let { user } = this.state;
    if (window.localStorage.getItem('basic_auth')) {
      return user ? user : { user: 'nobody' };
    } else return null;
  }

  getUserInfo = async (cached = true) => {
    if (window.localStorage.getItem('basic_auth') && this.state.user) {
      if (cached) return this.state.user;
      let { user } = await API.Auth.getCurrentUser();
      this.setState({ user });
      return user;
    } else if (window.localStorage.getItem('basic_auth')) {
      let { user } = await API.Auth.getCurrentUser();
      this.setState({ user });
      return user;
    } else {
      let error = new Error('Failed to get user info');
      Object.assign(error, { response: { status: 401 } });
      throw error;
    }
  };

  login = async (username, password) => {
    try {
      let { user } = await API.Auth.login(username, password);
      window.localStorage.setItem(
        'basic_auth',
        window.btoa(`${username}:${password}`)
      );
      this.setState({ user });
    } catch (err) {
      console.error(err.response);
    }
  };

  logout = async () => {
    this.setState({ user: null });
    window.localStorage.removeItem('basic_auth');
  };
}

export default AuthStore;
