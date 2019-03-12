import { request } from './utils';
import pick from 'lodash.pick';

const Auth = {
  login: (username, password) =>
    request.post('/auth', null, {
      headers: {
        Authorization: `Basic ${window.btoa(`${username}:${password}`)}`,
      },
    }),
  signup: (username, email, password) =>
    request.post('/auth/signup', {
      username,
      email,
      password,
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
  sendFriendRequest: (author, friend) => {
    let filteredAuthor = pick(author, ['id', 'url', 'host']);
    let filteredFriend = pick(friend, ['id', 'url', 'host']);
    return request.post('/friendrequest', {
      query: 'friendrequest',
      author: filteredAuthor,
      friend: filteredFriend,
    });
  },
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

const Search = {
  getUsers: () => request.get('/users'),
};

export { Auth, Post, Friend, Search };
