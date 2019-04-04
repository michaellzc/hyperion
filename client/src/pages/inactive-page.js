import React from 'react';
import styled, { createGlobalStyle } from 'styled-components/macro';
import { Link } from '@reach/router';
import AppLayout from '../components/app-layout';
import { Exception } from 'ant-design-pro';

let Wrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 75vh;
`;

let GlobalStyle = createGlobalStyle`
  @media (max-width: 768px) {
    .antd-pro-exception-imgBlock {
      display: none;
    }

    .antd-pro-exception-content {
      margin-top: 15vh;
      max-width: 80vw;
    }
  }
`;

function InactivePage() {
  return (
    <AppLayout header={false}>
      <GlobalStyle />
      <Wrapper>
        <Exception
          title="Pending Approval"
          desc="Please contact admin to activate your account"
          backText="Home"
          linkElement={Link}
        />
      </Wrapper>
    </AppLayout>
  );
}

export default InactivePage;
