import React, { useReducer } from 'react';
import UIcontainer from '../utils/uicontainer';
import { Form, Icon, Input, Modal, Row, Col } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import 'draft-js-static-toolbar-plugin/lib/plugin.css';

var initialProfile1;
let reducer = (state, action) => {
  switch (action.type) {
    case 'email':
      return { ...state, email: action.text };
    case 'bio':
      return { ...state, bio: action.text };
    case 'host':
      return { ...state, host: action.text };
    case 'firstName':
      return { ...state, firstName: action.text };
    case 'lastName':
      return { ...state, lastName: action.text };
    case 'displayName':
      return { ...state, displayName: action.text };
    case 'username':
      return { ...state, username: action.text };
    case 'url':
      return { ...state, url: action.text };
    case 'github':
      return { ...state, github: action.text };
    case 'reset':
      return initialProfile1;
    default:
      throw new Error();
  }
};

const ProfileBox = ({
  stores: [authStore, uiContainer],
  form: { getFieldDecorator, validateFields, setFieldsValue, getFieldValue },
  visible,
  toggleModal,
  initialProfile,
}) => {
  initialProfile1 = initialProfile;
  let [state, dispatch] = useReducer(reducer, initialProfile);
  // User cannot change the username and password
  let username = authStore.user.username;
  // User can change the following field
  let displayName = authStore.user.displayName;
  let email = authStore.user.email;
  let bio = authStore.user.bio;
  let github = authStore.user.github;

  let onUpdate = async () => {
    console.log(state);
    console.log(initialProfile);
    let {
      email,
      bio,
      host,
      firstName,
      lastName,
      displayName,
      url,
      github,
      username,
    } = state;
    try {
      console.log(initialProfile);
      console.log(state);
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
      dispatch({ type: 'reset' });
    } catch (error) {
      console.error(error);
    }
    dispatch({ type: 'reset' });
    console.log(initialProfile);
    console.log(initialProfile1);
    console.log(state);
    // console.log(changed);
    // changed = false;
    toggleModal();
  };

  let onCancel = () => {
    toggleModal();
    resetModal();
    // changed = false;
  };

  let resetModal = () => {
    //TODO:reset to correct user profile
    setFieldsValue({
      displayName: authStore.user.displayName,
    });
    setFieldsValue({
      email: authStore.user.email,
    });
    setFieldsValue({
      bio: authStore.user.bio,
    });
    setFieldsValue({
      github: authStore.user.github,
    });
  };
  let onInputChange = e => {
    dispatch({ type: e.target.name, text: e.target.value });
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
                    required: true,
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

export default inject([AuthStore, UIcontainer])(
  Form.create({ name: 'profile-box' })(ProfileBox)
);
