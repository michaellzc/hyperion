import { Container } from 'unstated';

class UIContainer extends Container {
  state = {
    isVisible: false,
  };

  toggleBox = () => {
    this.setState({ isVisible: !this.state.isVisible });
  };
}

export default UIContainer;
