import React, { useState } from 'react';
import UIcontainer from '../utils/uicontainer';

import { Form, Icon, Input, Modal } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import 'draft-js-static-toolbar-plugin/lib/plugin.css';

const ProfileBox = ({
  stores: [authStore, uiContainer],
  form: { getFieldDecorator, validateFields },
}) => {
  // let onLogin = async e => {
  //   e.preventDefault();

  //   validateFields(async (err, values) => {
  //     if (!err) {
  //       let { username, password } = values;

  //       await authStore.login(username, password);

  //       // redirect
  //       let { from } = parse(window.location.search);
  //       if (from) {
  //         await navigate(from);
  //       }
  //     }
  //   });
  // };

  let [isVisible, setVisibility] = useState(true);

  let onEdit = () => {};

  let toggleModal = () => {
    setVisibility(!isVisible);
    // uiContainer.toggleBox();
  };

  return (
    <div>
      <Modal
        title="Profile"
        visible={isVisible}
        onOk={onEdit}
        onCancel={toggleModal()}
      >
        <Form.Item>
          {getFieldDecorator('username')(
            <Input
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Username"
            />
          )}
        </Form.Item>
        <Form.Item>
          {getFieldDecorator('password')(
            <Input
              prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
              type="password"
              placeholder="Password"
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
