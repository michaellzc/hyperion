import React, { Fragment, useEffect, useState } from 'react';
import { navigate } from '@reach/router';
import { css } from 'styled-components/macro';
import { message, Icon, Tooltip, Dropdown, Menu, Empty, Spin } from 'antd';
import { PostStore, AuthStore } from '../stores';
import { inject } from '../utils';
import PostCard from './post-card';
import TextCardContent from './text-card-content';
import ImageCardContent from './image-card-content';
import MarkdownCardContent from './markdown-card-content';
import CardActionsFooter from './card-actions-footer';
import PostOverlay from './post-overlay';
import ProfileOverlay from './profile-popover';

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

const PostsStream = ({
  authorId: currentAuthorId,
  postId: openPostId = null,
  stores: [postStore, authStore],
  ...props
}) => {
  let [isVisible, setVisibility] = useState(false);
  let [postId, setPostId] = useState(null);
  let [isLoading, setLoading] = useState(false);

  let loadPosts = async () => {
    setLoading(true);
    if (currentAuthorId === undefined) {
      await postStore.getAll();
    } else {
      await postStore.getAuthorPosts(currentAuthorId);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (openPostId) {
      setPostId(openPostId);
      setVisibility(true);
    }
    loadPosts();
  }, [props.props.location]);

  // TODO - implement reply
  let handleReply = async event => {
    // https://stackoverflow.com/a/2385180
    // Prevent onClick event propagation to outter div
    event.stopPropagation();
  };

  let handleShare = async (event, origin) => {
    event.stopPropagation();

    let result = await navigator.permissions.query({ name: 'clipboard-write' });
    if (result.state === 'granted' || result.state === 'prompt') {
      try {
        await navigator.clipboard.writeText(origin);
        message.info('Copied to clipboard');
      } catch (err) {
        message.err('Oopps! Something went wrong');
      }
    } else {
      message.error('Your browser does not support Clipboard API.');
    }
  };

  let handleOpenPost = id => {
    setVisibility(true);
    navigate(`/posts/${id}`);
  };

  let toggleOverlay = () => {
    navigate('/');
    setVisibility(false);
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
      postsList.map(
        ({ id, contentType, author: user, origin, comments, ...props }) => (
          <PostCard
            key={id}
            id={id}
            avatar={<ProfileOverlay author={user} />}
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
                  ) : !window.OUR_HOSTNAME.includes(user.host) ? (
                    <Tooltip title={`Post from ${user.host}`}>
                      <Icon style={{ float: 'right' }} type="info-circle" />
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
                repliesCnt={comments ? comments.length : 0}
                onReply={e => handleReply(e, id)}
                onShare={e => handleShare(e, origin)}
              />
            }
          />
        )
      )
    ) : (
      <Empty />
    );

  return (
    <Fragment>
      {isLoading ? <Loading /> : posts}
      <PostOverlay
        postId={openPostId || postId}
        isVisible={isVisible}
        onCancel={toggleOverlay}
      />
    </Fragment>
  );
};

export default inject([PostStore, AuthStore])(PostsStream);
