import React, { Fragment, useEffect, useState } from 'react';
import { css } from 'styled-components/macro';
import { Empty, Spin, Button, Row, Col } from 'antd';
import { AuthStore, FriendsStore } from '../stores';
import { inject } from '../utils';
import FriendCard from './friend-card';

// Comment out username for now as API does not supply this field
const CardMetaTitle = ({ displayName, extra }) => (
  <Fragment>
    <span
      css={css`
        font-size: 20px;
      `}
    >
      {displayName}
    </span>
    <span
      css={css`
        float: right;
      `}
    >
      {extra}
    </span>
    <div
      css={css`
        padding-top: 16px;
        font-size: 14px;
        color: #777f88;
        font-weight: normal;
      `}
    >
      Hello, my name is {displayName}
    </div>
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
  stores: [authStore, friendStore],
}) => {
  //   let [postId, setPostId] = useState(null);
  let [isLoading, setLoading] = useState(false);

  let loadFriends = async () => {
    setLoading(true);
    let str = authStore.user.id;
    let id = str.split('https://cmput404-front.herokuapp.com/author/')[1];
    await friendStore.getFriends(id);
    setLoading(false);
    console.log(friendStore.friends);
  };

  useEffect(() => {
    loadFriends();
  }, []);

  let handleUnfriend = id => {
    console.log('unfriend clicked');
    console.log(id);
  };

  let friendList = friendStore.friends;
  let friends =
    friendList.length > 0 ? (
      friendList.map(({ id, displayName }) => (
        <Col xs={22} sm={22} md={12} lg={12} xl={12} xxl={12}>
          <FriendCard
            key={id}
            id={id}
            onLoad={handleUnfriend}
            metaTitle={
              <CardMetaTitle
                id={id}
                displayName={displayName}
                extra={
                  <Button onClick={() => handleUnfriend(id)}>Unfriend</Button>
                }
              />
            }
          />
        </Col>
      ))
    ) : (
      <Empty />
    );

  return (
    <Fragment>
      {isLoading ? (
        <Loading />
      ) : (
        <Row gutter={24} type="flex" justify="left" align="top">
          {friends}
        </Row>
      )}
    </Fragment>
  );
};

export default inject([AuthStore, FriendsStore])(FriendList);
