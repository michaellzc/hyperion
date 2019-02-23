import React, { Fragment } from 'react';
import styled from 'styled-components/macro';
import Markdown from 'react-remarkable';

let Title = styled.div`
  margin: 16px 0;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 500;
`;

const MarkdownCardContent = ({ title, content }) => {
  return (
    <Fragment>
      <Title>{title}</Title>
      <Markdown source={content} />
    </Fragment>
  );
};

export default MarkdownCardContent;
