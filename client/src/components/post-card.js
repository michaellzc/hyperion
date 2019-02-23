import React from 'react';
import { Card } from 'antd';
import './post-card.scss';

let { Meta } = Card;

// Content can be any react component
// - text
// - image
const PostCard = ({ metaTitle, avatar, content, footer }) => (
  <Card bordered={false}>
    <Meta avatar={avatar} title={metaTitle} />
    {content()}
    {footer}
  </Card>
);

export default PostCard;
