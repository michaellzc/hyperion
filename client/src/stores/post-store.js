import { Container } from 'unstated';

// TODO
// This should includes all post attributes
// class Post {
// }

class PostsStore extends Container {
  state = {
    // TODO
    posts: [
      {
        id: 1,
        user: {
          displayName: 'Michael Lin',
          username: '@michael.lin',
        },
        title: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',
        body:
          'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. ',
        replies: [],
      },
      {
        id: 2,
        user: {
          displayName: 'Lily',
          username: '@lily',
        },
        title: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',
        body:
          'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. ',
        replies: [],
      },
      {
        id: 3,
        user: {
          displayName: 'Haotian',
          username: '@haotian',
        },
        title: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',
        body:
          'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. ',
        replies: [],
      },
    ],
  };

  get posts() {
    return this.state.posts;
  }

  // TODO
  /**
   * etch all public posts
   * @param {bool} cached - Whether or not to re-fetch posts from remote
   */
  getAll = async (cached = true) => {};

  // TODO
  /**
   * Fetch a post by post ID
   * @param {id} id - Post id
   */
  get = async id => {};

  // TODO
  /**
   * Create a new post
   * @param {object} post - A post object
   */
  create = async post => {};
}

export default PostsStore;
