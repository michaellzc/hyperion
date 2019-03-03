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

const Post = {
  fetchAll: () => request.get('/author/posts'),
  create: post => request.post('/author/posts', { query: 'createPost', post }),
};

export { Auth, Post };
