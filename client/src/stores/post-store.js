import { Container } from 'unstated';
import fakePosts from './post.fixture';

// TODO
// This should includes all post attributes
// class Post {
// }

class PostsStore extends Container {
  state = {
    // TODO
    posts: new Map(),
  };

  get posts() {
    return [...this.state.posts.values()];
  }

  // TODO
  /**
   * etch all public posts
   * @param {bool} cached - Whether or not to re-fetch posts from remote
   */
  getAll = async (cached = true) => {
    if (cached && this.state.posts.length > 0) return;
    let delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    await delay(400);
    // let posts = new Map();
    let { posts } = this.state;
    fakePosts.map(post => posts.set(post.id, post));
    this.setState({
      posts,
    });
  };

  // TODO
  /**
   * Fetch a post by post ID
   * @param {id} id - Post id
   */
  get = async id => {
    let post = this.state.posts.get(id);
    if (!post) {
      // TODO - fetch post if not exist
    }
    // return post;
  };

  // TODO
  /**
   * Create a new post
   * @param {object} post - A post object
   */
  create = async post => {};

  /**
   * Add a comment to a post
   * @param {string} postId - The post id
   */
  addComment = async postId => {};
}

export default PostsStore;
