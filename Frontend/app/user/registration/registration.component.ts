import { Component } from '@angular/core';
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
  isLoading = false;

  constructor(public userService: UserService){
  }

  newModel() {
    this.model = new RegistrationModel('', '', '');
  }

  submit() {
    this.isLoading = true;
    this.userService.register(this.model).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    this.isLoading = false;
    this.regSuccess = true;
  }

  handleError(err) {
    this.isLoading = false;
    let data = err.json();
    this.newModel();
    let alertMessage = "Registation Failed:\n"
    for (let error of data['errors']) {
      alertMessage += "Title:" + error['title'] + ", Message:" + error['message'] + "\n";
    }
    alert(alertMessage);
  }
}
