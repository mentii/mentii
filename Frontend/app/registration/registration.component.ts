import { Component } from '@angular/core';
import {Http, Response, Headers, RequestOptions} from "@angular/http";
import {RegistrationModel} from './registration.model';
import {MentiiConfig} from '../mentii.config';

@Component({
  moduleId: module.id,
  selector: 'register-form',
  templateUrl: 'registration.html'
})

export class RegistrationComponent {
  model = new RegistrationModel('', '', '');
  mentiiConfig = new MentiiConfig();
  regSuccess = false;

  constructor(public http: Http){
  }

  newModel() {
    this.model = new RegistrationModel('', '', '');
  }

  submit() {
    let url = this.mentiiConfig.getRootUrl() + '/register/';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    let body = {
      "email": this.model.email,
      "password": this.model.password
    }


    /* TODO: Move this out to some sort of user.service.ts that will handle registration, signin, changing permissions, logout, etc. */
    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post(url, body, headers).subscribe(
      // TODO: Handle failure or errors
      (res:any)=>{
        let data = res.json();
        if (data !== 'Failing Registration Validation') {
          this.regSuccess = true;
        }
      }
      // TODO: Handle success better that current
    )
  }
}
