import { Container } from 'unstated';
import { EditorState, ContentState, convertFromRaw } from 'draft-js';
import { markdownToDraft } from 'markdown-draft-js';

let initialState = {
  title: null,
  description: null,
  content: null,
  visibility: 'PRIVATE',
  visibleTo: [],
  unlisted: false,
};

class UIStore extends Container {
  state = {
    isPostBoxVisible: false,
    editingPost: initialState,
    editorState: EditorState.createEmpty(),
  };

  togglePostBox = () => {
    let { isPostBoxVisible } = this.state;
    this.setState({ isPostBoxVisible: !isPostBoxVisible });
  };

  setEditingPost = post => {
    if (
      post.contentType === 'text/plain' ||
      post.contentType === 'text/markdown'
    ) {
      // Restore a DraftJS object from the markdown string
      this.setState({
        editorState: EditorState.createWithContent(
          convertFromRaw(markdownToDraft(post.content))
        ),
      });
    }
    post.visibleTo = post.visibleTo.map(post => post.id);
    this.setState({ editingPost: post });
  };

  setEditorState = editorState => {
    this.setState({ editorState });
  };

  updateEditingPost = action => {
    let { editingPost: state, editorState } = this.state;
    switch (action.type) {
      case 'title':
        this.setState({ editingPost: { ...state, title: action.text } });
        break;
      case 'description':
        this.setState({ editingPost: { ...state, description: action.text } });
        break;
      case 'content':
        this.setState({ editingPost: { ...state, content: action.text } });
        break;
      case 'visibility':
        this.setState({ editingPost: { ...state, visibility: action.text } });
        break;
      case 'visibleTo':
        this.setState({ editingPost: { ...state, visibleTo: action.text } });
        break;
      case 'unlisted':
        this.setState({ editingPost: { ...state, unlisted: action.checked } });
        break;
      case 'reset':
        this.setState({
          editingPost: initialState,
          editorState: EditorState.push(
            editorState,
            ContentState.createFromText('')
          ),
        });
        break;
      default:
        throw new Error();
    }
  };
}

export default UIStore;
