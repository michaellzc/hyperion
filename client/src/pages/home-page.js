import React from 'react';
import { Row, Col } from 'antd';
import AppLayout from '../components/app-layout';
import PostsStream from '../components/posts-stream';
import PostBox from '../components/post-box';

const HomePage = ({ postId, ...props }) => {
  if (postId) {
    postId = parseInt(postId) || encodeURIComponent(postId);
  }
  return (
    <AppLayout className="home-page" props={props}>
      <Row gutter={24} type="flex" justify="space-around" align="middle">
        <Col xs={20} sm={20} md={18} lg={12} xl={8} xxl={8}>
          <PostBox />
          <PostsStream postId={postId} props={props} />
        </Col>
      </Row>
    </AppLayout>
  );
};

export default HomePage;
