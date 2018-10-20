console.log('Hello')

class RequestMaker {

  get(url) {
    const req = new XMLHttpRequest();
    return new Promise((resolve, reject) => {
      req.open('GET', url, true);
      // set event listener for a change in the httpRequest's readystate
      req.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status >= 200 && this.status < 300) {
            resolve(this.response);
          } else {
            reject(this.response);
          }
        }
      };
      req.send();
    });
  }

  post(url, data) {
    const body = data ? JSON.stringify(data) : {};
    const req = new XMLHttpRequest();
    return new Promise((resolve, reject) => {
      req.open('POST', url, true);
      req.onreadystatechange = function() {
        if (this.readyState == 4) {
          if (this.status >= 200 && this.status < 300) {
            resolve(this.response);
          } else {
            reject(this.response);
          }
        }
      }
      // Must set request headers AFTER request is opened
      req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      req.setRequestHeader('Content-Type', 'application/json');
      req.send(body);
    });
  }
}

