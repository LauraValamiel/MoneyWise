import Cookies from 'js-cookie';

//const storage = {};

// Safari in incognito has local storage, but size 0
// This system falls back to cookies in that situation
interface StorageHandler {
  set: (key: string, value: any) => void;
  get: (key: string) => any;
  remove: (key: string) => void;
}

/*const storage: StorageHandler = {
  set: () => {},
  get: () => null,
  remove: () => {}
};
*/
/*
try {
  if (!window.localStorage) {
    throw Error('no local storage');
  }

  // Setup simple local storage wrapper
  storage.set = (key: string, value: any) => {
    localStorage.setItem(key, JSON.stringify(value));
  };

  storage.get = (key: string) => {
    const item = localStorage.getItem(key);
    try {
      return item ? JSON.parse(item) : null;
    } catch (e) {
      return null;
    }
  };

  storage.remove = (key: string) => {
    localStorage.removeItem(key);
  };
} catch (e) {
  storage.set = (key: string, value: any) => {
    Cookie.set(key, value);
  };
  
  storage.get = (key: string) => {
    return Cookie.getJSON(key);
  };
  
  storage.remove = (key: string) => {
    Cookie.remove(key);
  };
}*/

const storage: StorageHandler = {
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      Cookies.set(key, JSON.stringify(value));
    }
  },
  get: (key) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      return Cookies.get(key) ? JSON.parse(Cookies.get(key) as string) : null;
    }
  },
  remove: (key) => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      Cookies.remove(key);
    }
  }
};


export default storage;

