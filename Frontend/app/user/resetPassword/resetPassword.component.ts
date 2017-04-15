import { Component, OnInit, OnDestroy } from '@angular/core';
import { MentiiConfig } from '../../mentii.config';
import { UserService } from '../user.service';
import { ToastrService } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'reset-password-form',
  templateUrl: 'resetPassword.html'
})

export class ResetPasswordComponent implements OnInit, OnDestroy {
  private routeSub: any;
  resetPasswordId = '';
  passwordReset = false;
  isLoading = false;
  emailAddress = "";
  passwordVal = '';
  confirmPasswordVal = '';

  constructor(public userService: UserService, public toastr: ToastrService, private activatedRoute: ActivatedRoute,) {
  }

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.resetPasswordId = params['id'];
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  submit() {
    this.isLoading = true;
    this.userService.resetPassword(this.resetPasswordId, this.emailAddress, this.passwordVal).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleError(err) {
    this.isLoading = false;
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }

  handleSuccess() {
    this.isLoading = false;
    this.passwordReset = true;
  }

}
