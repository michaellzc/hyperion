import React, { useEffect, useState } from 'react';
import { Card, Icon } from 'antd';
import * as API from '../api';
import './profile-card.scss';

const ProfileCard = ({ authorId, ...props }) => {
  let [loading, setLoading] = useState(false);
  let [user, setAuthorProfile] = useState(null);

  let fetchAuthorProfile = async () => {
    setLoading(true);
    let author = await API.Author.getAuthorById(encodeURIComponent(authorId));
    setAuthorProfile(author);
    setLoading(false);
  };
  console.debug(authorId);
  useEffect(() => {
    fetchAuthorProfile();
  }, [authorId]);

  return (
    <Card
      className="profile-card"
      bordered={false}
      loading={loading}
      {...props}
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
        {user && user.github ? (
          <div className="github">
            <Icon type="github" />
            <a
              id="github1"
              href={user.github}
              target="_blank"
              rel="noopener noreferrer"
            >
              Github
            </a>
          </div>
        ) : null}
      </div>
    </Card>
  );
};

export default ProfileCard;
