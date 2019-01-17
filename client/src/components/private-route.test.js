import React from 'react';
import { mount } from 'enzyme';
import { Provider } from 'unstated';
import PrivateRoute from './private-route';
import { AuthStore } from '../stores';
import Login from '../pages/login-page';

function Dummpy() {
  return <div>Dummpy</div>;
}

it('should render Login', () => {
  let auth = new AuthStore();
  let wrapper = mount(
    <Provider inject={[auth]}>
      <PrivateRoute as={Dummpy} />
    </Provider>
  );
  expect(wrapper).toContainReact(<Login />);
});

it('should render Dummy', async () => {
  let auth = new AuthStore();

  window.localStorage.setItem('basic_auth', 'token');
  auth.state.user = 'dummy user';

  let wrapper = mount(
    <Provider inject={[auth]}>
      <PrivateRoute as={Dummpy} />
    </Provider>
  );

  let dummyElement = '<div>Dummpy</div>';
  expect(wrapper).toHaveHTML(dummyElement);
});
