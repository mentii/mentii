import { Component } from '@angular/core';
import {Response, Headers, RequestOptions} from "@angular/http";
import { AuthHttp } from '../utils/AuthHttp.service';
import {Router} from '@angular/router';
import {MentiiConfig} from '../mentii.config';

@Component({
  moduleId: module.id,
  selector: 'secure-test',
  templateUrl: 'secure-test.html'
})
export class SecureTestComponent {
  mentiiConfig = new MentiiConfig();

  constructor(public http: AuthHttp, public router: Router){
    this.testToken();
  }

  handleError(error){
    alert("Auth token failed. Service returned code: " + error.status + " " + error.statusText + ". Returning to Sign in.");
  }

  handleSuccess(data){
    alert("Auth token successful. You are: " + data.json().payload.user.email);
  }

  testToken () {
    // TODO: Store the auth token somewhere else and retrieve it from there
    let url = this.mentiiConfig.getRootUrl() + '/secure/';
    let body = {};

    /* TODO: Move this out to some sort of user.service.ts that will handle registration, signin, changing permissions, logout, etc. */
    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post(url, body)
    .subscribe(
      data => this.handleSuccess(data),
      err => this.handleError(err)
    );
  }
}
