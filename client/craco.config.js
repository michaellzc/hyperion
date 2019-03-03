const CracoLessPlugin = require('craco-less');

const ENV = process.env.NODE_ENV;

const babelPlugins = [
  [
    'babel-plugin-import',
    { libraryName: 'antd', libraryDirectory: 'es', style: true },
  ],
  [
    'babel-plugin-import',
    {
      libraryName: 'ant-design-pro',
      libraryDirectory: 'lib',
      style: true,
      camel2DashComponentName: false,
    },
    'ant-design-pro',
  ],
];

const babelTestPlugins = [];

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          modifyVars: {
            '@primary-color': '#4a4a4a',
          },
          javascriptEnabled: true,
        },
      },
    },
  ],
  babel: { plugins: ENV === 'test' ? babelTestPlugins : babelPlugins },
};
