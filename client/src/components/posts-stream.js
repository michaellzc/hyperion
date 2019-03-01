import React, { Fragment, useEffect, useState } from 'react';
import { css } from 'styled-components/macro';
import {
  Avatar,
  message,
  Icon,
  Tooltip,
  Dropdown,
  Menu,
  Empty,
  Spin,
} from 'antd';
import { PostStore, AuthStore } from '../stores';
import { inject } from '../utils';
import PostCard from './post-card';
import TextCardContent from './text-card-content';
import ImageCardContent from './image-card-content';
import MarkdownCardContent from './markdown-card-content';
import CardActionsFooter from './card-actions-footer';
import PostOverlay from './post-overlay';

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

const PostsStream = ({ stores: [postStore, authStore] }) => {
  let [isVisible, setVisibility] = useState(false);
  let [postId, setPostId] = useState(null);
  let [isLoading, setLoading] = useState(false);

  let loadPosts = async () => {
    setLoading(true);
    await postStore.getAll();
    setLoading(false);
  };

  useEffect(() => {
    loadPosts();
  }, []);

  // TODO - implement reply
  let handleReply = async (event, id) => {
    // https://stackoverflow.com/a/2385180
    // Prevent onClick event propagation to outter div
    event.stopPropagation();
    console.info('click reply button');
  };

  // TODO - copy link to clipboard
  let handleShare = async (event, id) => {
    event.stopPropagation();
    message.info('Copied to clipboard');
    console.info('click share button');
  };

  let handleOpenPost = id => {
    setVisibility(true);
    setPostId(id);
  };

  let toggleOverlay = () => {
    setVisibility(!isVisible);
  };

  let handleMenuClick = async (postId, { key, domEvent: e }) => {
    e.stopPropagation();
    if (key === 'delete') {
      await postStore.delete(postId);
    }
  };

  let postsList = postStore.posts;
  let posts =
    postsList.length > 0 ? (
      postsList.map(({ id, contentType, author: user, ...props }) => (
        <PostCard
          key={id}
          id={id}
          avatar={<Avatar icon="user" />}
          onClick={() => handleOpenPost(id)}
          metaTitle={
            <CardMetaTitle
              displayName={user.displayName}
              username={`@${user.username}`}
              extra={
                user.id === authStore.user.id ? (
                  <Tooltip title="more">
                    <Dropdown
                      overlay={
                        <Menu onClick={things => handleMenuClick(id, things)}>
                          <Menu.Item key="delete">Delete Post</Menu.Item>
                        </Menu>
                      }
                      onClick={e => e.stopPropagation()}
                      trigger={['click']}
                      placement="bottomRight"
                    >
                      <Icon style={{ float: 'right' }} type="down" />
                    </Dropdown>
                  </Tooltip>
                ) : null
              }
            />
          }
          content={() => {
            if (contentType === 'text/plain') {
              return <TextCardContent {...props} />;
            } else if (contentType.startsWith('image')) {
              return <ImageCardContent {...props} />;
            } else if (contentType === 'text/markdown') {
              return <MarkdownCardContent {...props} />;
            } else {
              throw new Error('Unsupported post content type.');
            }
          }}
          footer={
            <CardActionsFooter
              onReply={e => handleReply(e, id)}
              onShare={e => handleShare(e, id)}
            />
          }
        />
      ))
    ) : (
      <Empty />
    );

  return (
    <Fragment>
      {isLoading ? <Loading /> : posts}
      <PostOverlay
        postId={postId}
        isVisible={isVisible}
        onCancel={toggleOverlay}
      />
    </Fragment>
  );
};

export default inject([PostStore, AuthStore])(PostsStream);
