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
  fetch: id => request.get(`/posts/${id}`),
  create: post => request.post('/author/posts', { query: 'createPost', post }),
  delete: id => request.delete(`/posts/${id}`),
};

const Friend = {
  fetchFriendRequest: () => request.get('/friendrequest'),
  acceptFriendRequest: id =>
    request.put(`/friendrequest/${id}`, {
      query: 'friendrequestAction',
      accepted: true,
    }),
  declineFriendRequest: id =>
    request.put(`/friendrequest/${id}`, {
      query: 'friendrequestAction',
      accepted: false,
    }),
};

export { Auth, Post, Friend };
