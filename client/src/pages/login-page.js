import React from 'react';
import styled from 'styled-components/macro';
import { navigate, Link } from '@reach/router';
import { parse } from 'query-string';
import { Form, Icon, Input, Button, Row, Col } from 'antd';
import { AuthStore } from '../stores';
import { inject } from '../utils';
import AppLayout from '../components/app-layout';
import './login-page.scss';

let FormHeader = styled.div`
  text-align: center;
  margin: 20px 0;
  font-size: 32px;
  font-weight: 600;
`;

const LoginPage = ({
  stores: [authStore],
  form: { getFieldDecorator, validateFields },
}) => {
  let onLogin = async e => {
    e.preventDefault();

    validateFields(async (err, values) => {
      if (!err) {
        let { username, password } = values;

        await authStore.login(username, password);

        // redirect
        let { from } = parse(window.location.search);
        if (from) {
          await navigate(from);
        }
      }
    });
  };

  return (
    <AppLayout header={false} className="login-page">
      <Row gutter={24} type="flex" justify="space-around" align="middle">
        <Col span={6}>
          <FormHeader>A Social Distributioin Project</FormHeader>
          <Form onSubmit={onLogin} className="login-form">
            <Form.Item>
              {getFieldDecorator('username', {
                rules: [
                  { required: true, message: 'Please input your username!' },
                ],
              })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="Username"
                />
              )}
            </Form.Item>
            <Form.Item>
              {getFieldDecorator('password', {
                rules: [
                  { required: true, message: 'Please input your Password!' },
                ],
              })(
                <Input
                  prefix={
                    <Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  type="password"
                  placeholder="Password"
                />
              )}
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                Log in
              </Button>
              Or <Link to="register">register now!</Link>
            </Form.Item>
          </Form>
        </Col>
      </Row>
    </AppLayout>
  );
};

export default inject([AuthStore])(
  Form.create({ name: 'login_form' })(LoginPage)
);
