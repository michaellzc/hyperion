import React from 'react';
import { Card } from 'antd';
import './friend-card.scss';

let { Meta } = Card;

const FriendCard = ({ metaTitle, ...props }) => (
  <Card className="friend-card" bordered={false} {...props}>
    <Meta style={{ margin: '-4px -4px' }} title={metaTitle} />
  </Card>
);

export default FriendCard;
