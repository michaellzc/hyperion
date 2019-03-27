import React, { useState } from 'react';
import { bool, node, array } from 'prop-types';
import { Layout, Dropdown, Avatar, Menu, Icon } from 'antd';
import styled, { css } from 'styled-components/macro';
import { inject } from '../utils';
import { AuthStore } from '../stores';
import Notification from './notification';
import logo from '../assets/logo-horizontal.png';
import ProfileBox from '../components/profile-box';
import { navigate } from '@reach/router';

let { Header, Content, Footer } = Layout;

let RightContainer = styled.div`
  display: flex;
  align-items: center;
`;

let CustomLayout = styled(Layout)`
  min-height: 100vh;
  max-width: 100vw;
`;

let CustomHeader = styled(Header)`
  position: fixed;
  z-index: 1;
  width: 100%;
  background: #ffff !important;
  height: 72px !important;
  display: flex;
  justify-content: space-between;
  align-items: center;
  @media (max-width: 567px) {
    justify-content: flex-end;
  }
`;

let CustomContent = styled(Content)`
  margin-top: 80px;
  padding: 20px 0;
`;

let CustomFooter = styled(Footer)`
  text-align: center;
`;

const AppLayout = ({ children, stores: [authStore], header, ...props }) => {
  // TODO - implment logout
  let [visible, setVisible] = useState(false);

  let toggleProfile = () => {
    setVisible(!visible);
  };

  let redirect = e => {
    if (e.key === 'home') {
      navigate('/');
    } else if (e.key === 'profile') {
      navigate(
        `/${authStore.user.id.substr(authStore.user.id.lastIndexOf('/') + 1)}`
      );
    }
  };

  let menu = (
    <Menu className="menu" selectable={false}>
      <Menu.Item key="home" onClick={redirect}>
        <Icon type="home" />
        Home
      </Menu.Item>
      <Menu.Item key="settings" onClick={toggleProfile}>
        <Icon type="info-circle" />
        Settings
      </Menu.Item>
      <Menu.Item key="profile" onClick={redirect}>
        <Icon type="user" />
        Profile
      </Menu.Item>
      <Menu.Item key="logout" onClick={authStore.logout}>
        <Icon type="logout" />
        Logout
      </Menu.Item>
    </Menu>
  );

  return (
    <CustomLayout {...props}>
      {header ? (
        <CustomHeader>
          <img
            src={logo}
            alt="logo"
            css={css`
              max-height: 35px;
              height: 72px;
              line-height: 72px;
              @media (max-width: 567px) {
                display: none;
              }
            `}
          />
          <RightContainer>
            <Notification />
            <Dropdown overlay={menu}>
              <span className="action account">
                <Avatar
                  className="avatar"
                  icon="user"
                  style={{
                    margin: '20px 8px 20px 0',
                  }}
                />
                <span className="name">{authStore.user.displayName}</span>
              </span>
            </Dropdown>
            <ProfileBox visible={visible} toggleModal={toggleProfile} />
          </RightContainer>
        </CustomHeader>
      ) : null}
      <CustomContent>{children}</CustomContent>
      <CustomFooter>Copyright © 2019 CMPUT404W19T6</CustomFooter>
    </CustomLayout>
  );
};

AppLayout.propTypes = {
  children: node.isRequired,
  stores: array.isRequired,
  header: bool,
};

AppLayout.defaultProps = {
  header: true,
};

export default inject([AuthStore])(AppLayout);
