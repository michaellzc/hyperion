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

  let setBaseInfo = async () => {
    setLoading(true);
    // await authStore.getUserInfo(false);
    // https://www.reddit.com/r/javascript/comments/5abyi2/is_there_a_way_to_implement_sleep_with_es6/
    await sleep(1000);
    setLoading(false);
    let user = authStore.user;
    if (!user) return;
    document.getElementsByClassName('displayName')[0].innerHTML =
      user.displayName;
    document.getElementsByClassName('username')[0].innerHTML =
      '@' + user.username;
    if (user.bio === '') {
      document.getElementsByClassName('bio')[0].innerHTML =
        'Hello, my name is ' + user.displayName;
    } else {
      document.getElementsByClassName('bio')[0].innerHTML = user.bio;
    }
    if (authStore.user.github !== '') {
      console.log(authStore.user.github);
      document
        .getElementById('github1')
        .setAttribute('href', authStore.user.github);
    }
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
      <div className="userinfo">
        <div className="displayName" />
        <div className="username" />
        <div className="bio" />
        <div className="github">
          <Icon type="github" />
          <a id="github1">Github</a>
        </div>
      </div>
    </Card>
  );
};

export default inject([AuthStore])(ProfileCard);
