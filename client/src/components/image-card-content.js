import React, { Fragment } from 'react';
import styled from 'styled-components/macro';

let Title = styled.div`
  margin: 16px 0;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 500;
  font-size: 19px;
`;

let Content = styled.img`
  width: 100%;
  height: auto;
`;

const ImageCardContent = ({ title, content }) => {
  return (
    <Fragment>
      <Title>{title}</Title>
      <Content src={content} alt="image" />
    </Fragment>
  );
};

export default ImageCardContent;
