import React, { useState } from 'react';
import styled from 'styled-components/macro';
import { Link } from '@reach/router';
import { Avatar, Popover, Card, Button, message } from 'antd';
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
    try {
      await API.Friend.sendFriendRequest(authStore.user, author);
      message.info('Sent friend request.');
    } catch (error) {
      message.error('Opps! Please try again.');
    }
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
            <Link
              to={
                // Handling for authors from foreign servers
                window.OUR_HOSTNAME.includes(author.host)
                  ? `/${author.id.substr(author.id.lastIndexOf('/') + 1)}`
                  : `/${encodeURIComponent(author.id)}`
              }
            >
              {author.displayName}
            </Link>
          </UserField>
          <hr />
          <BioContainer>
            <p>{author.bio}</p>
          </BioContainer>
        </Wrapper>
      }
    >
      <Avatar icon="user" />
    </Popover>
  );
}

export default inject([AuthStore])(ProfilePopover);
