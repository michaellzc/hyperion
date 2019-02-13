import React, { useState, useRef, useReducer } from 'react';
import styled from 'styled-components/macro';
import PluginEditor from 'draft-js-plugins-editor';
import createMarkdownPlugin from 'draft-js-markdown-plugin';
import createToolbarPlugin from 'draft-js-static-toolbar-plugin';
import { draftToMarkdown } from 'markdown-draft-js';
import { EditorState, ContentState, convertToRaw } from 'draft-js';
import {
  Card,
  Modal,
  Avatar,
  Input,
  Radio,
  Icon,
  Row,
  Col,
  Tooltip,
  Tabs,
  Upload,
} from 'antd';
import { AuthStore, PostStore } from '../stores';
import { inject, colors } from '../utils';
import 'draft-js-static-toolbar-plugin/lib/plugin.css';

let CardWrapper = styled.div`
  margin: 0 0 16px 0;
`;

let InputPlaceHolder = styled.div`
  padding: 4px 11px;
  width: 95%;
  height: 32px;
  font-size: 14px;
  float: right;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.65);
  background-color: #fff;
  background-image: none;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  transition: all 0.3s;
  color: #d7d7d7;
  user-select: none;
  cursor: pointer;
`;

let EditorWrapper = styled.div`
  box-sizing: border-box;
  border: 1px solid #d9d9d9;
  cursor: text;
  padding: 16px;
  border-radius: 4px;
  margin: 2em 0;
  background: #fefefe;

  :hover {
    border-color: ${colors.primaryColor};
  }

  .public-DraftEditor-content {
    min-height: 140px;
  }

  .public-DraftEditorPlaceholder-inner {
    color: #cccccc;
  }
`;

let InputWrapper = styled.div`
  margin-top: 2em;
`;

let cardBodyStyle = {
  padding: '12px',
};

let visibilityOptions = [
  {
    value: 'PRIVATE',
    title: 'Only visible to me',
    iconType: 'lock',
  },
  {
    value: 'SERVERONLY',
    title: 'Only visible to your home server',
    iconType: 'bank',
  },
  {
    value: 'PUBLIC',
    title: 'Visible to everyone',
    iconType: 'global',
  },
  {
    value: 'FRIENDS',
    title: 'Visible to direct friends',
    iconType: 'user',
  },
  {
    value: 'FOAF',
    title: 'Visible to friends of friends',
    iconType: 'team',
  },
];

let reducer = (state, action) => {
  switch (action.type) {
    case 'title':
      return { ...state, title: action.text };
    case 'description':
      return { ...state, description: action.text };
    case 'content':
      return { ...state, content: action.text };
    case 'visibility':
      return { ...state, visibility: action.text };
    case 'reset':
      return initialState;
    default:
      throw new Error();
  }
};

let staticToolbarPlugin = createToolbarPlugin();
let markdownPlugin = createMarkdownPlugin();
let plugins = [staticToolbarPlugin, markdownPlugin];
let { Toolbar } = staticToolbarPlugin;

let { TabPane } = Tabs;

let UploadButton = (
  <div>
    <Icon type="plus" />
    <div className="ant-upload-text">Upload</div>
  </div>
);

let initialState = {
  title: null,
  description: null,
  content: null,
  visibility: 'PRIVATE',
};

const PostBox = ({ stores: [authStore, postStore] }) => {
  let [isVisisble, setVisibility] = useState(false);
  let [tabKey, setTabKey] = useState('text');
  let [fileList, setFileList] = useState([]);
  let [previewVisible, setPreviewVisible] = useState(false);
  let [previewImage, setPreviewImage] = useState('');
  let [editorState, setEditorState] = useState(EditorState.createEmpty());
  let [state, dispatch] = useReducer(reducer, initialState);

  let editorRef = useRef(null);

  let toggleModal = () => {
    setVisibility(!isVisisble);
  };

  let onEditorChange = editorState => {
    setEditorState(editorState);
    dispatch({
      type: 'content',
      text: draftToMarkdown(convertToRaw(editorState.getCurrentContent())),
    });
  };

  let onInputChange = e =>
    dispatch({ type: e.target.id || e.target.name, text: e.target.value });

  let onPost = async () => {
    let { title, description, content } = state;
    let contentType = 'text/markdown';
    try {
      if (tabKey === 'text') {
        // placeholder
      } else if (tabKey === 'image') {
        let file = fileList[0];
        contentType = `${file.type};base64`;
        content = fileList[0].thumbUrl;
      }
      await postStore.create({ title, description, content, contentType });
      dispatch({ type: 'reset' });
      setEditorState(
        EditorState.push(editorState, ContentState.createFromText(''))
      );
      setFileList([]);
      setPreviewImage(false);
      toggleModal();
    } catch (error) {
      console.error(error);
    }
  };

  let handleUploadPreview = file => {
    setPreviewImage(file.url || file.thumbUrl);
    setPreviewVisible(true);
  };

  let handleUploadChange = ({ fileList }) => setFileList(fileList);
  let handleUploadCancel = () => setPreviewVisible(false);

  return (
    <CardWrapper>
      <Card bordered={false} bodyStyle={cardBodyStyle}>
        <Row type="flex" justify="space-around" align="middle">
          <Col span={2}>
            <Avatar icon="user" />
          </Col>
          <Col span={22}>
            <InputPlaceHolder onClick={toggleModal}>What's up</InputPlaceHolder>
          </Col>
        </Row>
        <Modal
          visible={isVisisble}
          onCancel={toggleModal}
          maskClosable={false}
          onOk={onPost}
          okText="Post"
        >
          <Radio.Group
            name="visibility"
            onChange={onInputChange}
            value={state.visibility}
          >
            {visibilityOptions.map(({ title, value, iconType }) => (
              <Tooltip key={value} title={title}>
                <Radio.Button value={value}>
                  <Icon type={iconType} />
                </Radio.Button>
              </Tooltip>
            ))}
          </Radio.Group>
          <InputWrapper>
            <label htmlFor="title">Title</label>
            <Input
              id="title"
              type="text"
              value={state.title}
              onChange={onInputChange}
            />
          </InputWrapper>
          <InputWrapper>
            <label htmlFor="description">Description</label>
            <Input
              id="description"
              type="text"
              value={state.description}
              onChange={onInputChange}
            />
          </InputWrapper>
          <Tabs activeKey={tabKey} onChange={key => setTabKey(key)}>
            <TabPane
              tab={
                <span>
                  <Icon type="edit" />
                  text
                </span>
              }
              key="text"
            >
              <EditorWrapper
                ref={editorRef}
                onClick={() => editorRef.current.focus()}
              >
                <PluginEditor
                  editorState={editorState}
                  onChange={onEditorChange}
                  plugins={plugins}
                  placeholder="Support plaintext and markdown"
                />
                <Toolbar />
              </EditorWrapper>
            </TabPane>
            <TabPane
              tab={
                <span>
                  <Icon type="picture" />
                  image
                </span>
              }
              key="image"
            >
              <Upload
                accept="image/*"
                listType="picture-card"
                fileList={fileList}
                onPreview={handleUploadPreview}
                onChange={handleUploadChange}
                beforeUpload={file => {
                  setFileList([...fileList, file]);
                  return false;
                }}
              >
                {fileList.length >= 1 ? null : UploadButton}
              </Upload>
              <Modal
                visible={previewVisible}
                footer={null}
                onCancel={handleUploadCancel}
              >
                <img
                  alt="upload-preview"
                  style={{ width: '100%' }}
                  src={previewImage}
                />
              </Modal>
            </TabPane>
          </Tabs>
        </Modal>
      </Card>
    </CardWrapper>
  );
};

export default inject([AuthStore, PostStore])(PostBox);
