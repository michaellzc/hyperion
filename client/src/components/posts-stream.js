import React, { Fragment, useEffect } from 'react';
import { css } from 'styled-components/macro';
import { Avatar, message } from 'antd';
import { PostStore } from '../stores';
import { inject } from '../utils';
import PostCard from './post-card';
import TextCardContent from './text-card-content';
import ImageCardContent from './image-card-content';
import MarkdownCardContent from './markdown-card-content';
import CardActionsFooter from './card-actions-footer';

const CardMetaTitle = ({ displayName, username }) => (
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
  </Fragment>
);

const PostsStream = ({ stores: [postStore] }) => {
  useEffect(() => {
    postStore.getAll();
  });

  // TODO - implement reply
  const handleReply = async () => {
    console.info('click reply button');
  };

  // TODO - copy link to clipboard
  const handleShare = async () => {
    message.info('Copied to clipboard');
    console.info('click share button');
  };

  return postStore.posts.map(({ id, contentType, user, ...props }) => {
    return (
      <PostCard
        key={id}
        avatar={<Avatar icon="user" />}
        metaTitle={
          <CardMetaTitle
            displayName={user.displayName}
            username={user.username}
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
          <CardActionsFooter onReply={handleReply} onShare={handleShare} />
        }
      />
    );
  });
};

export default inject([PostStore])(PostsStream);
