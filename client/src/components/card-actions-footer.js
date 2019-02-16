import React from 'react';
import styled from 'styled-components/macro';
import { number, func } from 'prop-types';
import { Icon } from 'antd';

let HorizontalList = styled.ul`
  float: right;
  padding-top: 16px;
  list-style: none;
`;

let HorizontalListItem = styled.li`
  float: left;
  padding: 0 8px;
`;

let NoStyleButton = styled.button`
  all: unset;

  :hover {
    color: #408ff7;
  }
`;

let IconStyles = { fontSize: '16px' };

const CardActionsFooter = ({ repliesCnt, onReply, onShare }) => (
  <HorizontalList>
    <HorizontalListItem>
      <span>
        <NoStyleButton onClick={onReply}>
          <Icon type="message" alt="reply" style={IconStyles} />
        </NoStyleButton>{' '}
        {` `}
        {repliesCnt}
      </span>
    </HorizontalListItem>
    <HorizontalListItem>
      <span>
        <NoStyleButton onClick={onShare}>
          <Icon type="share-alt" alt="share" style={IconStyles} />
        </NoStyleButton>
      </span>
    </HorizontalListItem>
  </HorizontalList>
);

CardActionsFooter.propTypes = {
  repliesCnt: number,
  onReply: func.isRequired,
  onShare: func.isRequired,
};

CardActionsFooter.defaultProps = {
  repliesCnt: 0,
};

export default CardActionsFooter;
