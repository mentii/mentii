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

  constructor(public http: Http){
  }

  newModel() {
    this.model = new RegistrationModel('', '', '');
  }

  submit() {
    let url = this.mentiiConfig.rootUrl + '/register/';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    let body = {
      "email": this.model.email,
      "password": this.model.password
    }

    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post(url, body, headers).subscribe(
      (res:any)=>{
        let data = res.json();
      }
    )
  }
}
