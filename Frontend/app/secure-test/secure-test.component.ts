import { Component } from '@angular/core';
import {Http, Response, Headers, RequestOptions} from "@angular/http";
import {Router} from '@angular/router';
import {MentiiConfig} from '../mentii.config';

@Component({
  moduleId: module.id,
  selector: 'secure-test',
  templateUrl: 'secure-test.html'
})
export class SecureTestComponent {
  mentiiConfig = new MentiiConfig();

  constructor(public http: Http, public router: Router){
    this.testToken();
  }

  testToken () {
    // TODO: Store the auth token somewhere else and retrieve it from there
    let auth_token = localStorage.getItem("auth_token");
    let password = ''; // this is unused but needed for 'faking' the basic auth header
    let url = this.mentiiConfig.getRootUrl() + '/secure/';
    let headers = new Headers({"Authorization": "Basic " + btoa(auth_token+":"+password)});
    headers.append("Content-Type", 'application/json');
    let options = new RequestOptions({ headers: headers });
    let body = {}

    /* TODO: Move this out to some sort of user.service.ts that will handle registration, signin, changing permissions, logout, etc. */
    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post(url, body, options).subscribe(
      // TODO: Handle failure or errors
      (res:any)=>{
        let data = res.json();

        // TODO: Handle success better that current
        if (data.payload) {
          //TODO: Remove this, testing only
          console.log("user: " + data.payload);
          alert("your token works");

        } else {
          alert("no data payload from server");
        }

      }

    )
  }
}
