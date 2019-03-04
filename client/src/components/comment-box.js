import React, { useState } from 'react';
import styled from 'styled-components/macro';
import { Comment, Avatar, Form, Input, Button, Row, Col } from 'antd';

let Editor = ({ onChange, onSubmit, submitting, value }) => (
  <div>
    <Form.Item>
      <Input.TextArea
        onClick={e => {
          e.stopPropagation();
        }}
        rows={4}
        onChange={onChange}
        value={value}
      />
    </Form.Item>
    <Form.Item>
      <Button
        htmlType="submit"
        loading={submitting}
        onClick={onSubmit}
        type="primary"
        disabled={value ? false : true}
      >
        Reply
      </Button>
    </Form.Item>
  </div>
);

let InputPlaceHolder = styled.div`
  padding: 6px 11px;
  width: 95%;
  height: 36px;
  font-size: 14px;
  float: left;
  line-height: 1.5;
  color: #657786;
  background-color: #fff;
  background-image: none;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  transition: all 0.3s;
  user-select: none;
  cursor: pointer;
  margin-left: 6px;
`;

const CommentBox = ({ postId }) => {
  let [isEditing, setEditing] = useState(false);
  let [comment, setComment] = useState();
  let [submitting, setSubmitting] = useState(false);

  let toggleEditor = () => {
    setEditing(!isEditing);
  };

  let handleChange = e => {
    setComment(e.target.value);
  };

  let handleSubmit = async event => {
    // TODO
    let delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    setSubmitting(true);
    event.stopPropagation();
    console.info(`Add comment to ${postId}`);
    await delay(250);
    setSubmitting(false);
    setComment(null);
    setEditing(false);
  };

  return isEditing ? (
    <Comment
      onClick={toggleEditor}
      avatar={<Avatar icon="user" />}
      content={
        <Editor
          onChange={handleChange}
          onSubmit={handleSubmit}
          submitting={submitting}
          value={comment}
        />
      }
    />
  ) : (
    <Row
      type="flex"
      justify="space-around"
      align="middle"
      style={{ margin: '24px 0' }}
    >
      <Col span={2}>
        <Avatar icon="user" />
      </Col>
      <Col span={22}>
        <InputPlaceHolder onClick={toggleEditor}>
          Post your reply
        </InputPlaceHolder>
      </Col>
    </Row>
  );
};

export default CommentBox;
