This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Codebase Overview

### Folder structure

```
client/src/
├── api.js     # API requests
├── assets     # Static assets
├── components # Anything that are below the scope of a page
├── pages      # Pages
├── stores     # Global state management
└── utils      # Whatever methods or files you have no clue where to put. Hide your mess!
```

### Notes

Keep UI states local, unless they need to be shared across components.

Stuffs like fetching remote data, sending request to change backend data. They should be implemented with stores for the sake of consistency.

Avoid directory nesting, all components (anything but page component) should go under `components/` directory.

### How to make request to backend server

By default, frontend React App in development mode will proxy all request from `/api/*` to `http://127.0.0.1:8000`.

You may either spin up a local backend server at `http://127.0.0.1:8000`, which will work with the default configuration.

Or you may use the remote server, just overwrite the `proxy` attribute in [client/package.json](./package.json)

## Available Scripts

In the project directory, you can run:

### `yarn dev`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `yarn format`

Run `prettier` to format codes.

### `yarn lint --fix`

Run `eslint` to fix styling error.

### `yarn test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
