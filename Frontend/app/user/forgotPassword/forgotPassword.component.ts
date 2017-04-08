import { Component } from '@angular/core';
import { MentiiConfig } from '../../mentii.config';
import { UserService } from '../user.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  moduleId: module.id,
  selector: 'forgot-password-form',
  templateUrl: 'forgotPassword.html'
})

export class ForgotPasswordComponent {
  mentiiConfig = new MentiiConfig();
  emailSent = false;
  isLoading = false;
  emailAddress = "";

  constructor(public userService: UserService, public toastr: ToastrService){
  }

  submit() {
    this.isLoading = true;
    this.userService.forgotPassword(this.emailAddress).subscribe(
      data => this.handleSuccess(),
      err => this.handleSuccess()
    );
  }

  handleSuccess() {
    this.isLoading = false;
    this.emailSent = true;
  }

}
