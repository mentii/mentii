import { AuthHttp } from '../../utils/AuthHttp.service';
import { Component } from '@angular/core';
import { MentiiConfig } from '../../mentii.config';
import { Router } from '@angular/router';
import { SigninModel } from './signin.model';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { UserService } from '../user.service';

@Component({
  moduleId: module.id,
  selector: 'signin-form',
  templateUrl: 'signin.html'
})

export class SigninComponent {
  model = new SigninModel('', '');
  mentiiConfig = new MentiiConfig();
  isLoading = false;

  constructor(public userService: UserService, public authHttpService: AuthHttp , public router: Router, public toastr: ToastsManager){
  }

  handleSuccess(data) {
    this.isLoading = false;
    if (data.payload.token) {
      this.authHttpService.login(data.payload.token);
      this.authHttpService.saveRole(data.user.userRole);
      this.router.navigateByUrl('/dashboard');
    } else {
      alert("Success but no token. False authentication.");
    }
  }

  handleError(err) {
    this.toastr.error("Unrecgonized email or password.");
    this.isLoading = false;
  }

  submit() {
    this.isLoading = true;
    this.userService.signIn(this.model)
    .subscribe(
      data => this.handleSuccess(data.json()),
      err => this.handleError(err)
    );
  }
}
