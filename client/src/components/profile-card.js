import React, { useEffect, useState } from 'react';
import { inject } from '../utils';
import { Card, Icon } from 'antd';
import './profile-card.scss';
import { AuthStore } from '../stores';

const ProfileCard = ({ stores: [authStore], ...props }) => {
  let [loading, setLoading] = useState(false);
  let [displayName, setdisplayName] = useState('');
  let [username, setuserName] = useState('');
  let [bio, setuserBio] = useState('');
  let [github, setuserGithub] = useState('');

  let setBaseInfo = () => {
    setLoading(true);
    let user = authStore.user;
    if (!user) return;
    console.log(user.displayName);
    setdisplayName(user.displayName);
    setuserName(user.username);
    if (user.bio === '') {
      setuserBio('Hello, my name is ' + user.displayName);
    } else {
      setuserBio(user.bio);
    }

    setuserGithub(user.github);
    setLoading(false);
  };

  useEffect(() => {
    setBaseInfo();
  }, [authStore.user]);

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
      <div class="userinfo">
        <div class="displayName">{displayName}</div>
        <div class="username">@{username}</div>
        <div class="bio">{bio}</div>
        <div class="github">
          <Icon type="github" />
          {github === '' ? (
            <span id="github">Github</span>
          ) : (
            <a href={github} id="github">
              Github
            </a>
          )}
        </div>
      </div>
    </Card>
  );
};

export default inject([AuthStore])(ProfileCard);
