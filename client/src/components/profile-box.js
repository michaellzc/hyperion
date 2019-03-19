import React, { useEffect } from 'react';
import { Form, Icon, Input, Modal, Row, Col, message } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import pickby from 'lodash.pickby';

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
  };

  useEffect(() => {
    setBaseInfo();
  }, [authStore.user]);

  let onUpdate = async e => {
    e.preventDefault();
    validateFields(async (err, values) => {
      let validValues = pickby(
        values,
        val => val !== null && val !== undefined
      );
      if (!err) {
        try {
          await authStore.updateProfile(validValues);
          message.success('Profile updated.');
        } catch (error) {
          message.info('Opps! Please try again.');
          await authStore.getUserInfo(false);
        }
        toggleModal();
      }
    });
  };

  let onCancel = async () => {
    toggleModal();
    try {
      await authStore.getUserInfo(false);
    } catch (error) {}
  };

  return (
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
            {getFieldDecorator('username')(
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
        {getFieldDecorator('github', {
          rules: [
            {
              pattern: RegExp(/^https:\/\/github.com\/([\S]+)/),
              message: 'Invalid Github Url. e.g, https://github.com/username',
            },
          ],
        })(
          <Input
            name="github"
            prefix={<Icon type="github" style={{ color: 'rgba(0,0,0,.25)' }} />}
            placeholder="Github"
            type="url"
          />
        )}
      </Form.Item>
    </Modal>
  );
};

export default inject([AuthStore])(
  Form.create({ name: 'profile-box' })(ProfileBox)
);
