import React from 'react';
import UIcontainer from '../utils/uicontainer';
import { Form, Icon, Input, Modal, Row, Col } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import 'draft-js-static-toolbar-plugin/lib/plugin.css';

const ProfileBox = ({
  stores: [authStore, uiContainer],
  form: { getFieldDecorator, validateFields },
  visible,
  toggleModal,
}) => {
  let onEdit = () => {
    console.log('bbb');
    toggleModal();
  };
  // User can change the following field
  let username = authStore.user.username;
  // password
  let displayName = authStore.user.displayName;
  let firstName = authStore.user.firstName;
  let lastName = authStore.user.lastName;
  let email = authStore.user.email;
  let bio = authStore.user.bio;
  let github = authStore.user.github;

  // User cannot change the following field
  let url = authStore.user.url;
  let host = authStore.user.host;
  let id = authStore.user.id;
  let isActive = authStore.user.isActive;
  return (
    <div>
      <Modal
        title="Profile"
        visible={visible}
        onOk={onEdit}
        onCancel={toggleModal}
      >
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item>
              <label>User Name</label>
              {getFieldDecorator('userName', { initialValue: username })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="Username"
                />
              )}
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item>
              <label>Password</label>
              {getFieldDecorator('password')(
                <Input
                  prefix={
                    <Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  type="password"
                  placeholder="Password"
                />
              )}
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item>
              <label>First Name</label>
              {getFieldDecorator('firstName', { initialValue: firstName })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="FirstName"
                />
              )}
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item>
              <label>Last Name</label>
              {getFieldDecorator('lastName', { initialValue: lastName })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="LastName"
                />
              )}
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item>
              <label>Display Name</label>
              {getFieldDecorator('displayName', { initialValue: displayName })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="DisplayName"
                />
              )}
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item>
              <label>E-mail</label>
              {getFieldDecorator('email', { initialValue: email })(
                <Input
                  prefix={
                    <Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  type="email"
                  placeholder="E-mail"
                />
              )}
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <label>Biography</label>
          {getFieldDecorator('bio', { initialValue: bio })(
            <Input
              prefix={
                <Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="Biography"
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>Github</label>
          {getFieldDecorator('github', { initialValue: github })(
            <Input
              prefix={
                <Icon type="github" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="Github"
              type="url"
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>URL</label>
          {getFieldDecorator('url', { initialValue: url })(
            <Input
              prefix={<Icon type="link" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="URL"
              type="url"
              disabled="true"
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>Host</label>
          {getFieldDecorator('host', { initialValue: host })(
            <Input
              id="host"
              prefix={<Icon type="home" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Host"
              type="url"
              disabled="true"
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>ID</label>
          {getFieldDecorator('id', { initialValue: id })(
            <Input
              prefix={
                <Icon type="idcard" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="ID"
              disabled="true"
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>Is Active</label>
          {getFieldDecorator('isActive', { initialValue: isActive })(
            <Input
              prefix={
                <Icon
                  type="check-circle"
                  style={{ color: 'rgba(0,0,0,.25)' }}
                />
              }
              placeholder="isActive"
              disabled="true"
            />
          )}
        </Form.Item>
      </Modal>
    </div>
  );
};

export default inject([AuthStore, UIcontainer])(
  Form.create({ name: 'profile-box' })(ProfileBox)
);
