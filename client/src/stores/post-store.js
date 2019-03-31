import { Container } from 'unstated';
import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from 'snakecase-keys';
import normalize from 'normalize-url';
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
            id: encodeURIComponent(
              normalize(`${post.author.host}/posts/${post.id}`)
            ),
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

  getGithubStream = async username => {
    let events = await API.Post.getGithubEvents(username);
    events = camelcaseKeys(events, { deep: true });
    let { posts } = this.state;
    events.forEach(event => {
      let post = {
        id: event.id,
        title: event.type,
        content: '## Preview not avaliable',
        description: '',
        contentType: 'text/markdown',
        source: `https://api.github.com/users/${username}/events`,
        origin: `https://api.github.com/users/${username}/events`,
        published: event.createdAt,
        github: true,
        author: {
          id: `https://api.github.com/users/${username}`,
          url: `https://api.github.com/users/${username}`,
          displayName: event.actor.login,
          username: event.actor.login,
          host: 'https://github.com',
        },
      };
      posts.set(post.id, post);
    });
    this.setState({ posts });
  };

  // TODO
  /**
   * Fetch a post by post ID
   * @param {id} id - Post id
   */
  get = async (id, cached = true) => {
    let post = this.state.posts.get(id);
    if (!post || !cached) {
      let {
        posts: [resp],
      } = await API.Post.fetch(id);
      let { posts } = this.state;
      if (!window.OUR_HOSTNAME.includes(resp.author.host)) {
        // foreign post
        // overwrite post.id to `http(s)://<foreign_hostname>/posts/<id>`
        // then escape post.id and post.author.id to play well in actual URL.
        resp = {
          ...resp,
          id: encodeURIComponent(
            normalize(`${resp.author.host}/posts/${resp.id}`)
          ),
          author: {
            ...resp.author,
            id: resp.author.id,
          },
        };
        posts.set(resp.id, resp);
      } else {
        // local post
        posts.set(resp.id, resp);
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
