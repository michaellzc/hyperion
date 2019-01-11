import { request } from './utils';

const Auth = {
  login: (username, password) =>
    request.post('/auth', null, {
      headers: {
        Authorization: `Basic ${window.btoa(`${username}:${password}`)}`,
      },
    }),
  getCurrentUser: () => request.get('/auth'),
};

export { Auth };
