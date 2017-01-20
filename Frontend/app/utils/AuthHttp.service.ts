import { Injectable } from '@angular/core';
import { Http, XHRBackend, RequestOptions, Request, RequestOptionsArgs, Response, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';


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

  constructor (backend: XHRBackend, options: RequestOptions, private router: Router, public toastr: ToastsManager ) {
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
      if (res.status === 401) {
        this.toastr.error("You must sign in to view this page", "Authentication Error");
        this.logout(); //remove bad auth token from local storage
        this.router.navigateByUrl(''); // return to signin
        res["isAuthenticationError"] = true;
      } else if (res.status === 403) {
        this.toastr.error("You do not have permission to view this page", "Insufficient Privileges");
        this.router.navigateByUrl(''); // return to sign in or dashboard
        res["isAuthenticationError"] = true;
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
  }

  /**
  * Service method to load the auth token
  * @return {String} token
  */
  loadAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_NAME);
  }

  /**
   * Removes auth token from local storage
   * Updates the isAuthenticated flag throughout app to false
   */
  logout() {
    this.removeAuthToken();
    this._isAuthenticated.next(false);
  }

  /**
   * Saves the auth token to local storage
   * Updates the isAuthenticated flag throughout app to true
   * @param  {String} token
   */
  login(token) {
    this.saveAuthToken(token);
    this._isAuthenticated.next(true);
  }

  /**
   * Checks the current authentication status and
   * updates the isAuthenticated flag accordingly
   */
  checkAuthStatus() {
    let authStatus = false; // default to false. Would rather reject an authenticated user than allow anyone
    if (this.loadAuthToken() != null){
      this._isAuthenticated.next(true);
      authStatus = true;
    } else {
      this._isAuthenticated.next(false);
      authStatus = false;
    }
    return authStatus;
  }
}
