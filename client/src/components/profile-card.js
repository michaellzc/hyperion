import React from 'react';
import { Card } from 'antd';
import './post-card.scss';

let { Meta } = Card;

const ProfileCard = ({ metaTitle, avatar, content, footer, ...props }) => (
  <Card className="profile-card" bordered={false} {...props}>
    <Meta avatar={avatar} title={metaTitle} />
    {content()}
    {footer}
  </Card>
);

export default ProfileCard;
