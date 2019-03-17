import React, { useEffect } from 'react';
import { Form, Icon, Input, Modal, Row, Col, message } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import 'draft-js-static-toolbar-plugin/lib/plugin.css';

const ProfileBox = ({
  stores: [authStore],
  form: { getFieldDecorator, validateFields, setFieldsValue, getFieldsValue },
  visible,
  toggleModal,
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

  let onUpdate = async e => {
    e.preventDefault();
    validateFields(async (err, values) => {
      if (!err) {
        try {
          await authStore.updateProfile(values);
          await authStore.getUserInfo(false);
          message.success('Profile updated.');
        } catch (error) {
          console.error(error);
          message.info(
            'Something went wrong while updating user profile, please try again.'
          );
          await authStore.getUserInfo(false);
        }
        toggleModal();
      } else {
        console.log(err);
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
              {getFieldDecorator('userName')(
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
              {getFieldDecorator('displayName')(
                <Input
                  name="displayName"
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
              {getFieldDecorator('email', {
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
                  disabled={false}
                />
              )}
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <label>Biography</label>
          {getFieldDecorator('bio')(
            <Input
              name="bio"
              prefix={
                <Icon type="solution" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="Biography"
            />
          )}
        </Form.Item>
        <Form.Item>
          <label>Github</label>
          {getFieldDecorator('github')(
            <Input
              name="github"
              prefix={
                <Icon type="github" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="Github"
              type="url"
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
