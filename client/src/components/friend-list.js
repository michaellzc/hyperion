import React, { Fragment, useEffect, useState } from 'react';
import { css } from 'styled-components/macro';
import { Empty, Spin, Button, Row, Col, message } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import * as API from '../api';
import FriendCard from './friend-card';

// Comment out username for now as API does not supply this field
const CardMetaTitle = ({ displayName, bio, extra }) => (
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
      {bio || `Hi, this is ${displayName}`}
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

const FriendList = ({ authorId, stores: [authStore] }) => {
  let [isLoading, setLoading] = useState(false);
  let [friendList, setFriendList] = useState([]);

  let fetchFriendList = async () => {
    setLoading(true);
    // TODO(fixme)
    // - backend API is flawed, it should be authors instead of author
    if (!authorId.startsWith('https')) {
      let { authors } = await API.Friend.fetchFriendList(authorId);
      setFriendList(authors);
    } else {
      // Workaround, since /author/:id/friends does not support server-to-server request
      message.warn('External author friend list is not supported.');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchFriendList();
  }, [authorId]);

  let handleUnfriend = async friendId => {
    try {
      await API.Friend.unfriend(
        {
          id: authStore.user.id,
        },
        {
          id: friendId,
        }
      );
      message.info('Successfuly unfriend.');
    } catch (error) {
      message.error('Opps! Please try again.');
    }
    fetchFriendList();
  };

  let friends =
    friendList.length > 0 ? (
      friendList.map(({ id, bio, displayName }) => (
        <Col key={id} xs={22} sm={22} md={12} lg={12} xl={12} xxl={12}>
          <FriendCard
            id={id}
            onLoad={handleUnfriend}
            metaTitle={
              <CardMetaTitle
                id={id}
                displayName={displayName}
                bio={bio}
                extra={
                  // do not render unfriend button
                  authStore.userPk === authorId ? (
                    <Button onClick={() => handleUnfriend(id)}>Unfriend</Button>
                  ) : null
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
        <Row gutter={24} type="flex" justify="start" align="top">
          {friends}
        </Row>
      )}
    </Fragment>
  );
};

export default inject([AuthStore])(FriendList);
