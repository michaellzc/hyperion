import React from 'react';
import { Subscribe } from 'unstated';

const inject = _containers => Component => props => (
  <Subscribe to={_containers}>
    {(...containers) => <Component {...props} stores={containers} />}
  </Subscribe>
);

export default inject;
