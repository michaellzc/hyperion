import React, { Fragment, useEffect, useState } from 'react';
import { css } from 'styled-components/macro';
import { Empty, Spin, Button, Row, Col } from 'antd';
import { PostStore, AuthStore, FriendsStore } from '../stores';
import { inject } from '../utils';
import FriendCard from './friend-card';

// Comment out username for now as API does not supply this field
const CardMetaTitle = ({ displayName, username, extra }) => (
  <Fragment>
    {displayName}{' '}
    <small
      css={css`
        font-weight: lighter;
        padding-left: 8px;
      `}
    >
      {username}
    </small>
    {extra}
  </Fragment>
);

const Loading = () => (
  <div
    css={css`
      text-align: center;
    `}
  >
    <Spin size="large" />
  </div>
);

const FriendList = ({
  //   postId: openPostId,
  stores: [postStore, authStore, friendStore],
}) => {
  //   let [postId, setPostId] = useState(null);
  let [isLoading, setLoading] = useState(false);

  let loadFriends = async () => {
    setLoading(true);
    let str = authStore.user.id;
    let id = str.split('https://cmput404-front.herokuapp.com/author/')[1];
    await friendStore.getFriends(id);
    setLoading(false);
    let friendList = friendStore.friends;
    console.log(friendList);
    console.log(friendList.length);
  };

  useEffect(() => {
    loadFriends();
  }, []);

  let handleUnfriend = id => {
    console.log('unfriend clicked');
  };

  let friendList = friendStore.friends;
  let friends =
    friendList.length > 0 ? (
      friendList.map(
        ({ id, contentType, displayName, origin, comments, ...props }) => (
          <Col xs={22} sm={22} md={12} lg={12} xl={12} xxl={12}>
            <FriendCard
              key={id}
              id={id}
              metaTitle={
                <CardMetaTitle
                  displayName={displayName}
                  extra={<Button onClick={handleUnfriend}>Unfriend</Button>}
                />
              }
            />
          </Col>
        )
      )
    ) : (
      <Empty />
    );

  return (
    <Fragment>
      {isLoading ? (
        <Loading />
      ) : (
        <Row gutter={24} type="flex" justify="center" align="top">
          {friends}
        </Row>
      )}
    </Fragment>
  );
};

export default inject([PostStore, AuthStore, FriendsStore])(FriendList);
