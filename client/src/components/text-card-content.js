import React, { Fragment } from 'react';
import styled from 'styled-components/macro';

let Title = styled.div`
  margin: 16px 0;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 500;
`;

// TODO
// maybe tweak around line wrap
let Body = styled.div``;

const TextCardContent = ({ title, content }) => (
  <Fragment>
    <Title>{title}</Title>
    <Body>{content}</Body>
  </Fragment>
);

export default TextCardContent;
