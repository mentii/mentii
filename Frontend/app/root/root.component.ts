import { Component } from '@angular/core';
import {Http, Response, Headers, RequestOptions} from "@angular/http";
import {Router} from '@angular/router';
import {SigninModel} from './signin.model';
import {MentiiConfig} from '../mentii.config';

@Component({
  moduleId: module.id,
  selector: 'root',
  templateUrl: 'root.html'
})
export class RootComponent {
  model = new SigninModel('', '');
  mentiiConfig = new MentiiConfig();

  constructor(public http: Http, public router: Router){
  }

  submit() {
    let email = this.model.email;
    let password = this.model.password;
    let url = this.mentiiConfig.getRootUrl() + '/signin/';
    let headers = new Headers({"Authorization": "Basic " + btoa(email+":"+password)});
    headers.append("Content-Type", 'application/json');
    let options = new RequestOptions({ headers: headers });
    let body = {
    }

    /* TODO: Move this out to some sort of user.service.ts that will handle registration, signin, changing permissions, logout, etc. */
    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post(url, body, options).subscribe(
      // TODO: Handle failure or errors
      (res:any)=>{
        let data = res.json();

        // TODO: Handle success better that current
        if (data.payload.token) {
          //TODO: Remove this, testing only
          console.log("token: " + data.payload.token);

          // TODO: Store the auth token somewhere else
          localStorage.setItem("auth_token", data.payload.token);
          this.router.navigateByUrl('/secure-test');
        } else {
          alert("ya done fucked up");
        }

      }

    )
  }
}
