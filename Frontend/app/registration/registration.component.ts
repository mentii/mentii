import { Component } from '@angular/core';
import {Http, Response, Headers, RequestOptions} from "@angular/http";
import {registrationModel} from './registrationModel';

@Component({
  moduleId: module.id,
  templateUrl: 'registration.html'
})
export class RegistrationComponent {
  model = new registrationModel('', '', '');
  constructor(public http: Http){
  }
  onSubmit() {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    let body = {
      "email": this.model.email,
      "password": this.model.password
    }
    //this.http.post('http://api.mentii.me/register', this.model).subscribe(
    this.http.post('http://127.0.0.1:5000/register/', body, headers).subscribe(
      (res:any)=>{
        let data = res.json();

      }
    )
  }
}
