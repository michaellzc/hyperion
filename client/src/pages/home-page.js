import React from 'react';
import { Row, Col } from 'antd';
import AppLayout from '../components/app-layout';
import PostsStream from '../components/posts-stream';
import PostBox from '../components/post-box';

const HomePage = () => {
  return (
    <AppLayout className="home-page">
      <Row gutter={24} type="flex" justify="space-around" align="middle">
        <Col xs={20} sm={20} md={12} lg={10} xl={8} xxl={8}>
          <PostBox />
          <PostsStream />
        </Col>
      </Row>
    </AppLayout>
  );
};

export default HomePage;
