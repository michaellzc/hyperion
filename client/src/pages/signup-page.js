import React, { useState } from 'react';
import styled from 'styled-components/macro';
import { navigate, Link } from '@reach/router';
import { Form, Icon, Input, Button, Row, Col, Alert } from 'antd';
import { inject } from '../utils';
import { AuthStore } from '../stores';
import AppLayout from '../components/app-layout';

let FormHeader = styled.div`
  text-align: center;
  margin: 20px 0;
  font-size: 32px;
  font-weight: 600;
`;

function SignupPage({
  stores: [authStore],
  form: { getFieldDecorator, validateFields },
}) {
  let [error, setError] = useState(null);

  let signup = e => {
    e.preventDefault();

    validateFields(async (err, values) => {
      if (!err) {
        let { username, email, password } = values;
        try {
          await authStore.signup(username, email, password);
          navigate('/inactive');
        } catch (error) {
          setError('Username has been taken.');
        }
      }
    });
  };

  return (
    <AppLayout header={false} className="login-page">
      <Row gutter={24} type="flex" justify="space-around" align="middle">
        <Col xs={20} sm={20} md={12} lg={10} xl={8} xxl={6}>
          <FormHeader>A Social Distributioin Project</FormHeader>
          {error ? (
            <Alert
              message="Error"
              description={error}
              closable
              type="error"
              showIcon
            />
          ) : null}
          <Form onSubmit={signup} className="login-form">
            <Form.Item>
              {getFieldDecorator('email', {
                rules: [
                  {
                    type: 'email',
                    required: true,
                    message: 'Please input your email!',
                  },
                ],
              })(
                <Input
                  prefix={
                    <Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />
                  }
                  placeholder="hi@example.com"
                />
              )}
            </Form.Item>
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
                  { required: true, message: 'Please input your password!' },
                  { min: 8, message: 'Minimal 8 characters!' },
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
                Sign Up
              </Button>
              Already have an account? <Link to="/login">Log in here!</Link>
            </Form.Item>
          </Form>
        </Col>
      </Row>
    </AppLayout>
  );
}

export default inject([AuthStore])(
  Form.create({ name: 'signup_form' })(SignupPage)
);
