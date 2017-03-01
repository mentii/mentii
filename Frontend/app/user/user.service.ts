// Builtin
import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
// Services
import { AuthHttp } from '../utils/AuthHttp.service'
// Utilities
import { MentiiConfig } from '../mentii.config'
// Models
import { RegistrationModel } from '../user/registration/registration.model';
import { SigninModel } from '../user/signin/signin.model';
import { RoleModel } from '../admin/changeRole/role.model';

@Injectable()
export class UserService {
  mentiiConfig = new MentiiConfig();

  // This Service will need Http and AuthHttp
  constructor (private http: Http, private authHttp: AuthHttp) {
  }

  /**
  * Service method to register a user in the database
  * @param  {RegistrationModel} registrationModel Model representation of the registration form. Contains an email and password.
  * @return {Observable<any>}
  */
  register(registrationModel: RegistrationModel):Observable<any> {
    let registerUrl = this.mentiiConfig.getRootUrl() + '/register/';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    let body = {
      "email": registrationModel.email,
      "password": registrationModel.password
    }
    return this.http.post(registerUrl, body, options)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  /**
  * Service method to authenticate a user and get an auth token
  * @param  {SigninModel} signInModel Model representation of the sign in form. Contains an email and password
  * @return {Observable<any>}
  */
  signIn(signInModel: SigninModel):Observable<any> {
    let email = signInModel.email;
    let password = signInModel.password;
    let signinUrl = this.mentiiConfig.getRootUrl() + '/signin/';
    let headers = new Headers({"Authorization": "Basic " + btoa(email+":"+password)});
    headers.append("Content-Type", 'application/json');
    let options = new RequestOptions({ headers: headers });
    let body = {}
    return this.http.post(signinUrl, body, options)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  /**
  * Service method to change a user's role in the database
  * @param  {RoleModel} roleModel Model representation of the change user form. Contains an email and user role type.
  * @return {Observable<any>}
  */
  changeUserRole(roleModel: RoleModel):Observable<any> {
    let roleUrl = this.mentiiConfig.getRootUrl() + '/admin/changerole/';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    let body = {
      "email": roleModel.email,
      "userRole": roleModel.role
    }
    return this.authHttp.post(roleUrl, body, options)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  /**
  * Service method to add a class to a user and vice versa
  * @param  {string} classCode code of class user will join
  * @return {Observable<any>} data.json() will contain class title and code
  */
  joinClass(classCode) : Observable<any> {
    let joinClassUrl = this.mentiiConfig.getRootUrl() + '/user/classes/';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers })
    let body = {
      "code": classCode
    }
    return this.authHttp.post(joinClassUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }
}
