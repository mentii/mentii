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
  submitInprogress = false;
  regSuccess = false;

  constructor(public http: Http){
  }

  newModel() {
    this.model = new RegistrationModel('', '', '');
  }

  submit() {
    this.submitInprogress = true;

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
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    this.regSuccess = true;
  }

  handleError(err) {
    let data = err.json;
    this.submitInprogress = false;
    this.newModel();
    let alertMessage = "Registation Failed:\n"
    for (let error of data['errors']) {
      alertMessage += "Title:" + error['title'] + ", Message:" + error['message'] + "\n";
    }
    alert(alertMessage);
  }
}
