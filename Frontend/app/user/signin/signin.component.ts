import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SigninModel } from './signin.model';
import { MentiiConfig } from '../../mentii.config';
import { UserService } from '../user.service';
import { AuthHttp } from '../../utils/AuthHttp.service';

@Component({
  moduleId: module.id,
  selector: 'signin-form',
  templateUrl: 'signin.html'
})

export class SigninComponent {
  model = new SigninModel('', '');
  mentiiConfig = new MentiiConfig();

  constructor(public userService: UserService, public authHttpService: AuthHttp , public router: Router){
  }

  handleSuccess(data) {
    if (data.payload.token) {
      this.authHttpService.saveAuthToken(data.payload.token);
      this.router.navigateByUrl('/secure-test');
    } else {
      alert("Success but no token. False authentication");
    }
  }

  handleError(err) {
    alert("Sign in failed");
  }

  submit() {
    this.userService.signIn(this.model)
    .subscribe(
      data => this.handleSuccess(data.json()),
      err => this.handleError(err)
    );
  }
}
