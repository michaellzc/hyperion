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

function NotFoundPage() {
  return (
    <AppLayout header={false}>
      <Wrapper>
        <Exception
          title="Page Not Found"
          desc="Please try again"
          backText="Home"
          linkElement={Link}
        />
      </Wrapper>
    </AppLayout>
  );
}

export default NotFoundPage;
