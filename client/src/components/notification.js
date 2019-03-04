import React, { useState, useEffect } from 'react';
import styled from 'styled-components/macro';
import { Icon, Avatar, Button } from 'antd';
import { NoticeIcon } from 'ant-design-pro';
import * as API from '../api';
import { useInterval } from '../hooks';
import 'ant-design-pro/dist/ant-design-pro.css';

let StyledNoticeIcon = styled(NoticeIcon)`
  display: inline-block;
  height: 100%;
  padding: 12px 18px 0;
  cursor: pointer;
  transition: all 0.3s;
  > i {
    vertical-align: middle;
  }
  &:hover {
    background: rgba(0, 0, 0, 0.025);
  }
  &:global(.opened) {
    background: rgba(0, 0, 0, 0.025);
  }
`;

let Tab = styled(NoticeIcon.Tab)`
  &:hover {
    background: rgba(0, 0, 0, 0.025);
  }
  &:global(.opened) {
    background: rgba(0, 0, 0, 0.025);
  }
`;

let ButtonGroup = styled.div`
  display: flex;
  justify-content: space-between;
`;

let AlignLeft = styled.span`
  text-align: left;

  .ant-btn-primary {
    border-color: unset;
  }

  button {
    margin: 6px;
  }
`;

function Notification() {
  let [friendRequest, setFriendRequest] = useState([]);

  let handleConfirmFriendRequest = async id => {
    setFriendRequest(prev => prev.filter(each => each.id !== id));
    await API.Friend.acceptFriendRequest(id);
  };

  let handleDeleteFriendRequest = async id => {
    setFriendRequest(prev => prev.filter(each => each.id !== id));
    await API.Friend.declineFriendRequest(id);
  };

  let loadFriendRequest = async () => {
    let { frinedrequests: requests } = await API.Friend.fetchFriendRequest();
    let requestList = requests.map(each => ({
      id: each.id,
      avatar: <Avatar className="avatar" icon="user" />,
      title: each.author.display_name,
      description: (
        <ButtonGroup>
          <AlignLeft>
            <Button
              type="primary"
              onClick={() => handleConfirmFriendRequest(each.id)}
            >
              Confirm
            </Button>
            <Button onClick={() => handleDeleteFriendRequest(each.id)}>
              Delete
            </Button>
          </AlignLeft>
        </ButtonGroup>
      ),
    }));
    setFriendRequest(requestList);
  };

  useInterval(() => {
    loadFriendRequest();
  }, 5000);

  useEffect(() => {
    loadFriendRequest();
  }, []);

  return (
    <StyledNoticeIcon
      bell={<Icon style={{ fontSize: '24px' }} type="bell" />}
      count={friendRequest.length}
    >
      <Tab
        title="Friend Requests"
        emptyText="No pending request"
        showClear={false}
        list={friendRequest}
      />
    </StyledNoticeIcon>
  );
}

export default Notification;
