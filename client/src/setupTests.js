import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import 'jest-dom/extend-expect';

configure({ adapter: new Adapter() });

let mockStorage = {};

// https://gist.github.com/sanusart/c1558845350cc8d8cafbe3c903d46afc
window.localStorage = {
  setItem: (key, val) => Object.assign(mockStorage, { [key]: val }),
  getItem: key => mockStorage[key],
  clear: () => (mockStorage = {}),
};
