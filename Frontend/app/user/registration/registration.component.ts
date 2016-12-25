import { Component } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from "@angular/http";
import { RegistrationModel } from './registration.model';
import { MentiiConfig } from '../../mentii.config';
import { UserService } from '../user.service';

@Component({
  moduleId: module.id,
  selector: 'register-form',
  templateUrl: 'registration.html'
})

export class RegistrationComponent {
  model = new RegistrationModel('', '', '');
  mentiiConfig = new MentiiConfig();
  regSuccess = false;

  constructor(public http: Http, public userService: UserService){
  }

  newModel() {
    this.model = new RegistrationModel('', '', '');
  }

  submit() {
    this.userService.register(this.model).subscribe(
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
