import React from 'react';
import Sticky from 'react-stickynode';
import { Row, Col, Tabs } from 'antd';
import AppLayout from '../components/app-layout';
import FriendList from '../components/friend-list';
import ProfileCard from '../components/profile-card';
import PostsStream from '../components/posts-stream';

const TabPane = Tabs.TabPane;

// const AuthorProfilePage = ({ authorId, postId, ...props }) => {
const AuthorProfilePage = ({ authorId, ...props }) => {
  return (
    <AppLayout className="user-profile-page">
      <Row gutter={24} type="flex" justify="center" align="top">
        <Col xs={20} sm={8} md={8} lg={7} xl={6} xxl={6}>
          <Sticky enabled={true} top={80}>
            <ProfileCard
              authorId={authorId}
              location={props.location.pathname}
            />
          </Sticky>
        </Col>
        <Col xs={20} sm={15} md={14} lg={13} xl={11} xxl={10}>
          <Tabs type="card">
            <TabPane tab="Posts" key="1">
              <PostsStream authorId={authorId} props={props} />
            </TabPane>
            <TabPane tab="Friends" key="2">
              <FriendList authorId={authorId} />
            </TabPane>
          </Tabs>
        </Col>
      </Row>
    </AppLayout>
  );
};

export default AuthorProfilePage;
