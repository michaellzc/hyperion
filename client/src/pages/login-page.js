import React, { Component } from 'react';
import { navigate } from '@reach/router';
import { parse } from 'query-string';
import { css } from 'styled-components/macro';
import { AuthStore } from '../stores';
import { inject } from '../utils';

class LoginPage extends Component {
  state = {
    username: '',
    password: '',
  };

  onChange = e => {
    let { name, value } = e.target;
    this.setState({ [name]: value });
  };

  onLogin = async e => {
    e.preventDefault();

    let { username, password } = this.state;
    if (!username || !password) return;

    let [authStore] = this.props.stores;
    await authStore.login(username, password);

    // redirect
    let { from } = parse(window.location.search);
    if (from) {
      await navigate(from);
    }
  };

  render() {
    let { username, password } = this.state;

    return (
      <form
        onSubmit={this.onLogin}
        css={css`
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          display: flex;
          flex-wrap: wrap;
          flex-direction: column;
          align-items: center;
        `}
      >
        <label htmlFor="username">username: </label>
        <input
          name="username"
          id="username"
          type="text"
          value={username}
          onChange={this.onChange}
          autoComplete="username"
          required
        />
        <label htmlFor="password">password: </label>
        <input
          name="password"
          id="password"
          type="password"
          value={password}
          onChange={this.onChange}
          autoComplete="current-password"
          required
        />
        <button>Login</button>
      </form>
    );
  }
}

export default inject([AuthStore])(LoginPage);
