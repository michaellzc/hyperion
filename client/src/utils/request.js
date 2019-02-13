let { host, protocol } = window.location;
let API_ROOT = `${protocol}//${host}/api`;

let getDefaultHeaders = () => {
  const token = window.localStorage.getItem('basic_auth');
  return {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    Authorization: `Basic ${token}`,
  };
};

let errorHandler = async response => {
  if ([200, 201].includes(response.status)) return response.json();
  else {
    const errorBody = await response.json();
    const error = new Error(
      `Request failed with status code ${response.status}`
    );
    Object.assign(error, {
      response: {
        status: response.status,
        data: errorBody,
        headers: response.headers,
      },
    });
    throw error;
  }
};

let requests = {
  get: (url, opts = {}) => {
    let headers = getDefaultHeaders();
    return fetch(`${API_ROOT}${url}`, {
      ...opts,
      method: 'GET',
      headers: {
        ...headers,
        ...opts.headers,
      },
    }).then(errorHandler);
  },
  post: (url, data, opts = {}) => {
    let headers = getDefaultHeaders();
    return fetch(`${API_ROOT}${url}`, {
      ...opts,
      method: 'POST',
      headers: {
        ...headers,
        ...opts.headers,
      },
      body: JSON.stringify(data),
    }).then(errorHandler);
  },
  put: (url, data, opts = {}) => {
    let headers = getDefaultHeaders();
    return fetch(`${API_ROOT}${url}`, {
      ...opts,
      method: 'PUT',
      headers: {
        ...headers,
        ...opts.headers,
      },
      body: JSON.stringify(data),
    }).then(errorHandler);
  },
  delete: (url, opts = {}) => {
    let headers = getDefaultHeaders();
    return fetch(`${API_ROOT}${url}`, {
      ...opts,
      method: 'DELETE',
      headers: {
        ...headers,
        ...opts.headers,
      },
    }).then(errorHandler);
  },
};

export default requests;
