import React from 'react';
import { Card } from 'antd';
import './friend-card.scss';

let { Meta } = Card;

const FriendCard = ({ metaTitle, ...props }) => (
  <Card className="friend-card" bordered={false} {...props}>
    <Meta title={metaTitle} />
  </Card>
);

export default FriendCard;
