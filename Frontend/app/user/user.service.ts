import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { AuthHttp } from '../utils/AuthHttp.service'
import { MentiiConfig } from '../mentii.config'
import { RegistrationModel } from '../user/registration/registration.model';

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
    .map((res:Response) => res.json())
    .catch((error:any) => Observable.throw(error.json().error));
  }
}
