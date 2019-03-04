import React, { Fragment } from 'react';
import styled from 'styled-components/macro';

let Title = styled.div`
  margin: 16px 0;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 500;
  font-size: 19px;
`;

let Body = styled.div`
  font-size: 17px;
`;

const TextCardContent = ({ title, content }) => (
  <Fragment>
    <Title>{title}</Title>
    <Body>{content}</Body>
  </Fragment>
);

export default TextCardContent;
