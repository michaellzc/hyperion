import { Container } from 'unstated';
import camelcaseKeys from 'camelcase-keys';
// import snakecaseKeys from 'snakecase-keys';
import * as API from '../api';

class FriendsStore extends Container {
  state = {
    friends: new Map(),
  };
  get friends() {
    let { friends } = this.state;
    if (!friends) return null;
    return [...friends.values()];
  }

  getFriends = async id => {
    let { author: friendList, count } = await API.Friend.fetchFriendList(id);

    if (count > 0) {
      let { friends } = this.state;
      friendList = camelcaseKeys(friendList, { deep: true });
      friendList.forEach(friend => friends.set(friend.id, friend));
      this.setState({ friends });
    }
  };

  unfriend = async id => {};
}

export default FriendsStore;
