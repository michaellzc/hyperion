import { Container } from 'unstated';
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from 'snakecase-keys';
import * as API from '../api';

class PostsStore extends Container {
  state = {
    posts: new Map(),
  };

  get posts() {
    let { posts } = this.state;
    if (!posts) return null;
    return [...posts.values()].sort(
      (a, b) => new Date(b.lastModifyDate) - new Date(a.lastModifyDate)
    );
  }

  /**
   * etch all public posts
   * @param {bool} cached - Whether or not to re-fetch posts from remote
   */
  getAll = async (cached = true) => {
    if (cached && this.state.posts.length > 0) return;
    let { posts: postsList, count } = await API.Post.fetchAll();
    if (count > 0) {
      let { posts } = this.state;
      postsList = camelcaseKeys(postsList, { deep: true });
      postsList.forEach(post => posts.set(post.id, post));
      this.setState({ posts });
    }
  };

  // TODO
  /**
   * Fetch a post by post ID
   * @param {id} id - Post id
   */
  get = async id => {
    let post = this.state.posts.get(id);
    if (!post) {
      let { post: resp } = await API.Post.fetch(id);
      post = camelcaseKeys(resp);
      let { posts } = this.state;
      posts.set(post.id, post);
    }
  };

  /**
   * Create a new post
   * @param {object} post - A post object
   */
  create = async post => {
    return API.Post.create(snakecaseKeys(post));
  };

  /**
   * Delete a post
   * @param {id} id - Post id
   */
  delete = async id => {
    let { posts } = this.state;
    posts.delete(id);
    this.setState({ posts });
    await API.Post.delete(id);
  };

  /**
   * Add a comment to a post
   * @param {string} postId - The post id
   */
  addComment = async postId => {};
}

export default PostsStore;
