import { Injectable } from '@angular/core';
import { Http, XHRBackend, RequestOptions, Request, RequestOptionsArgs, Response, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';


const AUTH_TOKEN_NAME = "auth_token";

/**
* Used in place of the Http Service so that authentication headers
* and handling authenticaiton errors are not up to the component to handle.
* Otherwise works the exact same as the Http Service
* @return {[type]} [description]
*/
@Injectable()
export class AuthHttp extends Http {

  private _isAuthenticated = new BehaviorSubject<boolean>(false);
  isAuthenticated$ = this._isAuthenticated.asObservable();

  constructor (backend: XHRBackend, options: RequestOptions, private router: Router) {
    super(backend, options);
  }

  request(url: string|Request, options?: RequestOptionsArgs): Observable<Response> {
    let auth_token = this.loadAuthToken();
    let password = ''; // this is unused but needed for 'faking' the basic auth header
    let authHeaderString = 'Basic ' + btoa(auth_token+":"+password);
    if (typeof url === 'string') {
      if (!options) { // If options weren't specified in caller, initialize them here
        options = {
          headers: new Headers()
        };
      }options.headers.set('Authorization', authHeaderString);
    } else {
      // Probably won't be used but in place in case we use query strings
      url.headers.set('Authorization', authHeaderString);
    }
    return super.request(url, options).catch(this.catchAuthError(this));
  }

  private catchAuthError (self: AuthHttp) {
    return (res: Response) => {
      if (res.status === 401 || res.status === 403) {
        // If not authenticated return to signin
        this.logout();
        this.router.navigateByUrl('');
      }
      return Observable.throw(res);
    };
  }


  /**
  * Service method to remove the auth token
  */
  removeAuthToken() {
    // TODO: Should we store the auth token somewhere else?
    localStorage.removeItem(AUTH_TOKEN_NAME);
  }


  /**
  * Service method to save the auth token
  * @param {String} token
  */
  saveAuthToken(token) {
    // TODO: Should we store the auth token somewhere else?
    localStorage.setItem(AUTH_TOKEN_NAME, token);
    this.login(); //update isAuthenticated flag
  }

  /**
  * Service method to load the auth token
  * @return {String} token
  */
  loadAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_NAME);
  }

  logout() {
    this.removeAuthToken();
    this._isAuthenticated.next(false);
  }

  login() {
    this._isAuthenticated.next(true);
  }
}
