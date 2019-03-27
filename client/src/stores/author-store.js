import { Container } from 'unstated';
// import camelcaseKeys from 'camelcase-keys';
// import snakecaseKeys from 'snakecase-keys';
import * as API from '../api';

class AuthorStore extends Container {
  state = {
    author: null,
  };
  get author() {
    let { author } = this.state;
    if (!author) return null;
    return author;
  }

  getAuthor = async id => {
    let author = await API.Author.getauthorbyID(id);
    this.setState({ author });
  };
}

export default AuthorStore;
