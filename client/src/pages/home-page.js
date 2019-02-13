import React from 'react';
import { Row, Col } from 'antd';
import AppLayout from '../components/app-layout';
import PostsStream from '../components/posts-stream';

const HomePage = () => {
  return (
    <AppLayout>
      <Row gutter={24} type="flex" justify="space-around" align="middle">
        <Col span={12}>
          <PostsStream />
        </Col>
      </Row>
    </AppLayout>
  );
};

export default HomePage;
