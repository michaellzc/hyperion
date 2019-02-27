import React, { useEffect } from 'react';
import { Modal, List, Comment } from 'antd';
import { PostStore } from '../stores';
import { inject } from '../utils';
import TextCardContent from './text-card-content';
import MarkdownCardContent from './markdown-card-content';
import ImageCardContent from './image-card-content';
import CommentBox from './comment-box';

const PostOverlay = ({ postId, isVisible, onCancel, stores: [postStore] }) => {
  useEffect(() => {
    postStore.get(postId);
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
      {post ? content : null}
      <CommentBox postId={postId} />
      {post && post.comments.length > 0 ? (
        <List
          className="comment-list"
          itemLayout="horizontal"
          dataSource={post.comments}
          renderItem={item => (
            <Comment
              author={item.author.displayName}
              avatar={item.avatar}
              content={item.content}
            />
          )}
        />
      ) : null}
    </Modal>
  );
};

export default inject([PostStore])(PostOverlay);
