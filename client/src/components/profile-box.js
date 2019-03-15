import React, { useEffect } from 'react';
import { Form, Icon, Input, Modal, Row, Col } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import 'draft-js-static-toolbar-plugin/lib/plugin.css';

const ProfileBox = ({
  stores: [authStore],
  form: {
    getFieldDecorator,
    validateFields,
    setFieldsValue,
    getFieldValue,
    getFieldsValue,
  },
  visible,
  toggleModal,
  initialProfile,
}) => {
  let setBaseInfo = () => {
    let user = authStore.user;
    if (!user) return;
    Object.keys(getFieldsValue()).forEach(key => {
      const obj = {};
      obj[key] = user[key] || null;
      setFieldsValue(obj);
    });
    setFieldsValue({
      userName: authStore.user.username,
    });
  };
  useEffect(() => {
    setBaseInfo();
  }, [authStore.user]);

  // User cannot change the username and password
  var username = authStore.user.username;
  // User can change the following field
  var displayName = authStore.user.displayName;
  var email = authStore.user.email;
  var bio = authStore.user.bio;
  var github = authStore.user.github;
  var host = authStore.user.host;
  var firstName = authStore.user.firstName;
  var lastName = authStore.user.lastName;
  var url = authStore.user.url;

  let onUpdate = async e => {
    e.preventDefault();
    validateFields(async (err, values) => {
      if (!err) {
        try {
          email = getFieldValue('email');
          displayName = getFieldValue('displayName');
          bio = getFieldValue('bio');
          github = getFieldValue('github');
          await authStore.updateProfile({
            email,
            bio,
            host,
            firstName,
            lastName,
            displayName,
            url,
            github,
            username,
          });
          await authStore.getUserInfo(false);
        } catch (error) {
          console.error(error);
          await authStore.getUserInfo(false);
        }
        toggleModal();
      } else {
        console.log('Email format error');
      }
    });
  };

  let onCancel = async () => {
    toggleModal();
    try {
      await authStore.getUserInfo(false);
    } catch (error) {
      console.log(error);
    }
  };

  let onInputChange = e => {
    switch (e.target.name) {
      case 'email':
        email = e.target.value;
        return;
      case 'bio':
        bio = e.target.value;
        return;
      case 'displayName':
        displayName = e.target.value;
        return;
      case 'github':
        github = e.target.value;
        return;
      default:
        throw new Error();
    }
  };

  return (
    <div>
      <Modal
        title="Profile"
        visible={visible}
        onOk={onUpdate}
        onCancel={onCancel}
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
                  name="username"
                  disabled={true}
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
                  disabled={true}
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
                  name="displayName"
                  prefix={
                    <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="DisplayName"
                  onChange={onInputChange}
                />
              )}
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item>
              <label>E-mail</label>
              {getFieldDecorator('email', {
                initialValue: email,
                rules: [
                  {
                    type: 'email',
                    required: false,
                    message: 'Please enter a valid email!',
                  },
                ],
              })(
                <Input
                  name="email"
                  prefix={
                    <Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  type="email"
                  placeholder="E-mail"
                  onChange={onInputChange}
                  disabled={true}
                />
              )}
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <label>Biography</label>
          {getFieldDecorator('bio', { initialValue: bio })(
            <Input
              name="bio"
              prefix={
                <Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="Biography"
              onChange={onInputChange}
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>Github</label>
          {getFieldDecorator('github', { initialValue: github })(
            <Input
              name="github"
              prefix={
                <Icon type="github" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="Github"
              type="url"
              onChange={onInputChange}
            />
          )}
        </Form.Item>
      </Modal>
    </div>
  );
};

export default inject([AuthStore])(
  Form.create({ name: 'profile-box' })(ProfileBox)
);
