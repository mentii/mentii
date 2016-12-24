import { Component } from '@angular/core';
import {Http, Response, Headers, RequestOptions} from "@angular/http";
import {RegistrationModel} from './registration.model';
import {MentiiConfig} from '../../mentii.config';

@Component({
  moduleId: module.id,
  selector: 'register-form',
  templateUrl: 'registration.html'
})

export class RegistrationComponent {
  model = new RegistrationModel('', '', '');
  mentiiConfig = new MentiiConfig();
  submitDisabled = false;
  regSuccess = false;

  constructor(public http: Http){
  }

  newModel() {
    this.model = new RegistrationModel('', '', '');
  }

  submit() {
    this.submitDisabled = true;

    let url = this.mentiiConfig.getRootUrl() + '/register/';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    let body = {
      "email": this.model.email,
      "password": this.model.password
    }

    /* TODO: Move this out to some sort of user.service.ts that will handle registration, signin, changing permissions, logout, etc. */
    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post(url, body, options)
    .subscribe(
      data => this.handleSuccess(data.json()),
      err => this.handleError(err)
    );
  }

  handleSuccess(data) {
    if (data['errors'].length > 0) {
      this.submitDisabled = false;
      this.newModel();
      for (let error of data['errors']) {
        alert("Registation Failed:\n" + error['title']+": "+error['message']);
      }
    }
    else {
      this.regSuccess = true;
    }
  }

  handleError(err) {
    alert("Registration Failed")
    console.log(err);
  }
}
