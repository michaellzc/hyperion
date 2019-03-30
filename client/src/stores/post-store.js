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
      (a, b) => new Date(b.published) - new Date(a.published)
    );
  }

  /**
   * etch all public posts
   * @param {bool} cached - Whether or not to re-fetch posts from remote
   */
  getAll = async (cached = true) => {
    if (cached && this.state.posts.size > 0) return;
    let { posts: postsList, count } = await API.Post.fetchAll();
    if (count > 0) {
      let { posts } = this.state;
      postsList = camelcaseKeys(postsList, { deep: true });
      postsList.forEach(post => {
        if (!window.OUR_HOSTNAME.includes(post.author.host)) {
          // foreign post
          // overwrite post.id to `http(s)://<foreign_hostname>/posts/<id>`
          // then escape post.id and post.author.id to play well in actual URL.
          post = {
            ...post,
            id: encodeURIComponent(`${post.author.host}/posts/${post.id}`),
            author: {
              ...post.author,
              id: post.author.id,
            },
          };
          posts.set(post.id, post);
        } else {
          // local post
          posts.set(post.id, post);
        }
      });
      this.setState({ posts });
    }
  };

  /**
   * fetch all author's posts viewable by current user
   * @param {int} authorId
   */

  getAuthorPosts = async authorId => {
    // let { cached } = this.state;
    // if (cached === authorId && this.state.posts.size > 0) return;
    // clean state
    // if (cached && this.state.posts.size > 0) return;
    let response = await API.Post.fetchAuthorPosts(authorId);
    if (response.count > 0) {
      let { posts } = this.state;
      posts.clear();
      response.posts = camelcaseKeys(response.posts, { deep: true });
      response.posts.forEach(post => {
        if (!window.OUR_HOSTNAME.includes(post.author.host)) {
          // foreign post
          // overwrite post.id to `http(s)://<foreign_hostname>/posts/<id>`
          // then escape post.id and post.author.id to play well in actual URL.
          post = {
            ...post,
            id: encodeURIComponent(`${post.author.host}/posts/${post.id}`),
            author: {
              ...post.author,
              id: post.author.id,
            },
          };
          posts.set(post.id, post);
        } else {
          // local post
          posts.set(post.id, post);
        }
      });
      this.setState({ posts });
    }
  };

  // TODO
  /**
   * Fetch a post by post ID
   * @param {id} id - Post id
   */
  get = async (id, cached = true) => {
    let post = this.state.posts.get(id);
    if (!post || !cached) {
      let { post: resp } = await API.Post.fetch(id);
      post = camelcaseKeys(resp);
      let { posts } = this.state;
      if (!window.OUR_HOSTNAME.includes(post.author.host)) {
        // foreign post
        // overwrite post.id to `http(s)://<foreign_hostname>/posts/<id>`
        // then escape post.id and post.author.id to play well in actual URL.
        post = {
          ...post,
          id: encodeURIComponent(`${post.author.host}/posts/${post.id}`),
          author: {
            ...post.author,
            id: post.author.id,
          },
        };
        posts.set(post.id, post);
      } else {
        // local post
        posts.set(post.id, post);
      }
      this.setState({ posts });
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
  addComment = async (postId, author, text) => {
    let post = await this.state.posts.get(postId);
    let comment = {
      author,
      comment: text,
      contentType: 'text/plain',
    };
    if (!Number.isNaN(postId)) postId = 1;
    await API.Post.addComment(postId, post.source, comment);
  };
}

export default PostsStore;
