# CMPUT 404 Project

## Codebase Overview

### Technologies

Here is a list of all the big technologies we use:

- [**Django REST framework**](https://www.django-rest-framework.org/): REST API server
- [**ReactJS**](http://reactjs.org): Frontend React app, SPA
- [**Postgres**](https://www.postgresql.org/): Data storage

### Folder structure

```
cmput404_project/
├── api        # Django API server
├── infra      # Infrastructure stuffs, postgres, etc
└── client     # Frontend SPA
```

### Code Style

Rules

- All `.py` files must follow `PEP8`.
- All `.js` files must follow the preset `eslint` rules and format with `prettier`.
- All `.js` filenames should loosely follow such convention
  - `export default function HomePage;` -> `home.js` or `home-page.js`
  - `export default function variableName;` -> `variable-name.js`, `variable.js`, or `variablename.js` are all acceptable

Here is a few IDE plugins that can save your day!

- https://marketplace.visualstudio.com/items?itemName=ms-python.python
- https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
- https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig

## First time setup

### MacOS

The first step to running locally is installing Homebrew.

`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Also, you need `nvm` to manage node.js versions. For troubleshooting, follow [the nvm documentation](https://github.com/creationix/nvm).

`curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash`

#### Installation

```bash
# Install NodeJS
$ brew install node

# Install yarn, nodejs package management
$ brew install yarn

# Install python3
$ brew install python

# Optional, install https://postgresapp.com/
$ brew cask install postgres
```

#### Configuration

```bash
# Install NodeJS latest LTS version
$ nvm install 10

# Set default to 10
$ nvm alias default 10

# Setup python virtual environment
$ pip3 install --user virtualenv
$ virtualenv venv --python=python3
$ source venv/bin/activate
```

## Development

You may either run your own local postgres, or use the hosted development database. Check out connection info in [`infra/README.md`](./infra/README.md).

### Install dependencies

```bash
# Install python dependencies
$ pip install -r requirements.txt

# Install NodeJS dependencies
$ cd client
$ yarn
```

### Setup environment variable

```bash
$ cp .env.example .env

# Then modify the file as needed
$ source .env
```

### Start the project

```bash
# Run database migration if schema is changed
$ python manage.py migrate
# Create new super user if first time
$ python manage.py createsuperuser

# Launch django dev server
$ python manage.py runserver 8080

# Open a new tab in terminal
# Launch frontend dev server
$ cd client
$ yarn dev
```

## Deployment

API server is running at Heroku.

Frontend React app is hosted at Netlify.

Netlify will automatically deploy every commits in each branch, so you may check our the preview in no time.

Netlify will also proxy all HTTP request under `/api/*` to our backend server which is hosted at Heroku.

## LICENSE

[MIT](./LICENSE)
