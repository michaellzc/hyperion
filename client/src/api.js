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
  addComment: (id, url, comment) =>
    request.post(`/posts/${id}/comments`, {
      query: 'addComment',
      post: url,
      comment,
    }),
};

const Author = {
  getAuthorById: id => {
    return request.get(`/author/${id}`);
  },
  updateProfile: author => {
    let filteredProfile = pick(author, [
      'email',
      'bio',
      'github',
      'display_name',
    ]);
    return request.patch('/author', {
      query: 'updateProfile',
      author: filteredProfile,
    });
  },
};

const Friend = {
  fetchFriendRequest: () => request.get('/friendrequest'),
  sendFriendRequest: (author, friend) => {
    let filteredAuthor = pick(author, ['id', 'url', 'host', 'displayName']);
    let filteredFriend = pick(friend, ['id', 'url', 'host', 'displayName']);
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
  fetchFriendList: id => {
    return request.get(`/author/${id}/friends`);
  },
  unfriend: (author, friend) => {
    return request.post('/unfollow', {
      query: 'unfollow',
      author,
      friend,
    });
  },
};

const Search = {
  getUsers: () => request.get('/users'),
};

export { Auth, Post, Author, Friend, Search };
