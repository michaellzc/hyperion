import React from 'react';
import { render /* fireEvent */ } from 'react-testing-library';
import { Provider } from 'unstated';
import PostBox from './post-box';

it('should not render modal', () => {
  let { queryByText } = render(
    <Provider>
      <PostBox />
    </Provider>
  );
  expect(queryByText('Support plaintext and markdown')).not.toBeInTheDocument();
});

// it('should render modal', () => {
//   let { getByText } = render(
//     <Provider>
//       <PostBox />
//     </Provider>
//   );
//   fireEvent.click(getByText("What's up"));
//   expect(getByText('Support plaintext and markdown')).toBeInTheDocument();
//   expect(getByText('Support plaintext and markdown')).toBeVisible();
// });
