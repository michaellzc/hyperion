import React, { useEffect, useState } from 'react';
import { inject } from '../utils';
import { Card, Icon } from 'antd';
import './profile-card.scss';
import { AuthStore } from '../stores';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const ProfileCard = ({ stores: [authStore], ...props }) => {
  let [loading, setLoading] = useState(false);
  let user = authStore.user;

  let setBaseInfo = async () => {
    setLoading(true);
    await sleep(1000);
    setLoading(false);
  };

  useEffect(() => {
    setBaseInfo();
  }, []);

  return (
    <Card
      className="profile-card"
      bordered={false}
      {...props}
      loading={loading}
    >
      <Icon
        type="user"
        style={{ fontSize: '50px', color: '#aeb8c7' }}
        theme="outlined"
      />
      <div className="userinfo">
        <div className="displayName">{user ? user.displayName : ''}</div>
        <div className="username">{user ? '@' + user.username : ''}</div>
        <div className="bio">{user ? user.bio : ''}</div>
        <div className="github">
          <Icon type="github" />
          {user ? (
            <a id="github1" href={user.github}>
              Github
            </a>
          ) : (
            <a id="github1">Github</a>
          )}
        </div>
      </div>
    </Card>
  );
};

export default inject([AuthStore])(ProfileCard);
