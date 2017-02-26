import { Component } from '@angular/core';
import { Response, Headers, RequestOptions } from "@angular/http";
import { AuthHttp } from '../utils/AuthHttp.service';
import { Router } from '@angular/router';
import { MentiiConfig } from '../mentii.config';
import { ToastrService } from 'ngx-toastr';

@Component({
  moduleId: module.id,
  selector: 'secure-test',
  templateUrl: 'secureTest.html'
})
export class SecureTestComponent {
  mentiiConfig = new MentiiConfig();

  constructor(public http: AuthHttp, public router: Router, public toastr: ToastrService){
    this.testToken();
  }

  handleError(error){
    this.toastr.error("Auth token failed. Returning to Sign in.");
  }

  handleSuccess(data){
    var message = "Auth token successful. You are: " + data.json().payload.user.email;
    this.toastr.success(message);
  }

  testToken () {
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
