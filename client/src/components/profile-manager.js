import React, { useEffect } from 'react';
import { Modal, Form, Input, Icon, message } from 'antd';
import { inject } from '../utils';
import { AuthStore } from '../stores';

function ProfileManager({
  visible,
  toggleModal,
  stores: [authStore],
  form: { getFieldDecorator, validateFields, setFieldsValue, getFieldsValue },
}) {
  let setBaseInfo = () => {
    let user = authStore.user;
    Object.keys(getFieldsValue()).forEach(key => {
      const obj = {};
      obj[key] = user[key] || null;
      setFieldsValue(obj);
    });
  };

  let onSubmit = async e => {
    e.preventDefault();

    validateFields(async (err, values) => {
      if (!err) {
        try {
          await authStore.updateUserInfo(values);
          message.success('Profile updated.');
          toggleModal();
        } catch (error) {
          message.error('Opps! Please try again');
        }
      }
    });
  };

  useEffect(() => {
    setBaseInfo();
  }, [authStore.user]);

  return (
    <Modal
      title="Profile"
      okText="Save"
      onOk={onSubmit}
      visible={visible}
      onCancel={toggleModal}
    >
      <Form hideRequiredMark>
        <Form.Item label="Username">
          {getFieldDecorator('username', {
            rules: [{ required: true, message: 'Please input your username!' }],
          })(
            <Input
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Username"
            />
          )}
        </Form.Item>
        <Form.Item label="Display Name">
          {getFieldDecorator('displayName', {
            rules: [
              { required: true, message: 'Please input your display name!' },
            ],
          })(
            <Input
              prefix={<Icon type="tag" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Your name"
            />
          )}
        </Form.Item>
        <Form.Item label="Email">
          {getFieldDecorator('email', {
            rules: [
              { required: true, message: 'Please input your email!' },
              {
                type: 'email',
                required: true,
                message: 'Please input your email!',
              },
            ],
          })(
            <Input
              prefix={<Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="hi@example.com"
            />
          )}
        </Form.Item>
        <Form.Item label="Github">
          {getFieldDecorator('github', {
            rules: [{ type: 'url', message: 'Invalid URL!' }],
          })(
            <Input
              prefix={
                <Icon type="github" style={{ color: 'rgba(0,0,0,.25)' }} />
              }
              placeholder="https://github.com/username"
            />
          )}
        </Form.Item>
        <Form.Item label="Bio">
          {getFieldDecorator('bio')(
            <Input.TextArea placeholder="Your short bio" />
          )}
        </Form.Item>
      </Form>
    </Modal>
  );
}

export default inject([AuthStore])(
  Form.create({ name: 'update_profile_form' })(ProfileManager)
);
