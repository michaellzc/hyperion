import React from 'react';
import { Row, Col, Tabs } from 'antd';
import AppLayout from '../components/app-layout';
import PostsStream from '../components/posts-stream';
import FriendList from '../components/friend-list';

function callback(key) {
  console.log(key);
}
const TabPane = Tabs.TabPane;

const ProfilePage = ({ postId }) => {
  return (
    <AppLayout className="user-profile-page">
      <Row gutter={24} type="flex" justify="center" align="top">
        <Col xs={20} sm={8} md={8} lg={7} xl={6} xxl={6}>
          This is a place holder for user profile card.
        </Col>
        <Col xs={20} sm={15} md={14} lg={13} xl={11} xxl={10}>
          <Tabs onChange={callback} type="card">
            <TabPane tab="My Posts" key="1">
              <PostsStream postId={parseInt(postId)} />
            </TabPane>
            <TabPane tab="Friends" key="2">
              <FriendList />
            </TabPane>
          </Tabs>
        </Col>
      </Row>
    </AppLayout>
  );
};

export default ProfilePage;