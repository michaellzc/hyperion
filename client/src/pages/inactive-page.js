import React from 'react';
import styled from 'styled-components/macro';
import { Link } from '@reach/router';
import AppLayout from '../components/app-layout';
import { Exception } from 'ant-design-pro';

let Wrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 75vh;
`;

function InactivePage() {
  return (
    <AppLayout header={false}>
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
