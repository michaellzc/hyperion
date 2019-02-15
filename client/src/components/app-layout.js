import React from 'react';
import { bool, node, array } from 'prop-types';
import { Layout, Row, Col, Dropdown, Avatar, Menu } from 'antd';
import { css } from 'styled-components/macro';
import { inject } from '../utils';
import { AuthStore } from '../stores';
import logo from '../assets/logo-horizontal.png';

let { Header, Content, Footer } = Layout;

const AppLayout = ({ children, stores: [authStore], header, ...props }) => {
  // TODO - implment logout
  let menu = (
    <Menu className="menu" selectable={false}>
      <Menu.Item key="logout" onClick={authStore.logout}>
        Logout
      </Menu.Item>
    </Menu>
  );

  return (
    <Layout style={{ minHeight: '100vh', maxWidth: '100vw' }} {...props}>
      {header ? (
        <Header
          css={css`
            background: #ffff !important;
            height: 72px !important;
          `}
        >
          <Row gutter={24}>
            <Col span={4} offset={4}>
              <img
                src={logo}
                alt="logo"
                css={css`
                  max-height: 35px;
                `}
              />
            </Col>
            <Col span={4} offset={12}>
              <Dropdown overlay={menu}>
                <span className="action account">
                  <Avatar
                    className="avatar"
                    icon="user"
                    style={{
                      margin: '20px 8px 20px 0',
                    }}
                  />
                  <span className="name">{authStore.user.display_name}</span>
                </span>
              </Dropdown>
            </Col>
          </Row>
        </Header>
      ) : null}
      <Content style={{ padding: '20px 0' }}>{children}</Content>
      <Footer style={{ textAlign: 'center' }}>
        Copyright © 2019 CMPUT404W19T6
      </Footer>
    </Layout>
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
