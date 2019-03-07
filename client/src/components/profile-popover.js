import React, { useState } from 'react';
import styled from 'styled-components/macro';
import { Link } from '@reach/router';
import { Avatar, Popover, Card, Button } from 'antd';
import * as API from '../api';
import { AuthStore } from '../stores';
import { inject } from '../utils';

let Wrapper = styled.div`
  padding: 12px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  width: 250px;

  hr {
    width: 100%;
    background-color: white;
    border: 0;
  }
`;

let UserField = styled.div`
  a {
    font-weight: bold;
    font-size: 18px;
  }
`;

let BioContainer = styled.div``;

function ProfilePopover({ author, stores: [authStore] }) {
  let [loading, setLoading] = useState(false);

  let addFriend = async () => {
    setLoading(true);
    await API.Friend.sendFriendRequest(authStore.user, author);
    setLoading(false);
  };

  return authStore.user.username === author.username ? (
    <Avatar icon="user" />
  ) : (
    <Popover
      placement="bottomLeft"
      content={
        <Wrapper onClick={e => e.stopPropagation()}>
          <Card.Meta avatar={<Avatar icon="user" />} />
          <Button
            type="primary"
            icon="user-add"
            onClick={addFriend}
            loading={loading}
          />
          <hr />
          <UserField>
            <Link to={author.username}>{author.displayName}</Link>
          </UserField>
          <hr />
          <BioContainer>
            <p>It's lit!</p>
          </BioContainer>
        </Wrapper>
      }
    >
      <Avatar icon="user" />
    </Popover>
  );
}

export default inject([AuthStore])(ProfilePopover);
