import React, { useEffect } from 'react';
import { css } from 'styled-components/macro';
import { Modal, List, Comment, Spin } from 'antd';
import { PostStore } from '../stores';
import { inject } from '../utils';
import TextCardContent from './text-card-content';
import MarkdownCardContent from './markdown-card-content';
import ImageCardContent from './image-card-content';
import CommentBox from './comment-box';
import ProfilePopover from './profile-popover';

let Loading = () => (
  <div
    css={css`
      text-align: center;
    `}
  >
    <Spin size="large" />
  </div>
);

const PostOverlay = ({ postId, isVisible, onCancel, stores: [postStore] }) => {
  useEffect(() => {
    if (postId) {
      postStore.get(postId);
    }
  }, [postId]);

  let post = postStore.state.posts.get(postId);
  let content;

  if (post) {
    let { contentType } = post;
    if (contentType === 'text/plain') {
      content = <TextCardContent title={post.title} content={post.content} />;
    } else if (contentType.startsWith('image')) {
      content = <ImageCardContent title={post.title} content={post.content} />;
    } else if (contentType === 'text/markdown') {
      content = (
        <MarkdownCardContent title={post.title} content={post.content} />
      );
    } else {
      throw new Error('Unsupported post content type.');
    }
  }

  return (
    <Modal
      visible={isVisible}
      onCancel={onCancel}
      closable={false}
      footer={null}
    >
      {post ? content : <Loading />}
      <CommentBox postId={postId} />
      {post && post.comments.length > 0 ? (
        <List
          className="comment-list"
          itemLayout="horizontal"
          dataSource={post.comments.sort(
            (a, b) => new Date(b.published) - new Date(a.published)
          )}
          renderItem={item => (
            <Comment
              author={item.author.displayName}
              avatar={<ProfilePopover author={item.author} />}
              content={item.comment}
            />
          )}
        />
      ) : null}
    </Modal>
  );
};

export default inject([PostStore])(PostOverlay);
