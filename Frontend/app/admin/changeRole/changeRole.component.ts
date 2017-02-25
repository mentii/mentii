import { Component } from '@angular/core';
import { RoleModel } from './role.model';
import { UserService } from '../../user/user.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'changeRole',
  templateUrl: 'changeRole.html'
})

export class ChangeRole {
  model = new RoleModel('','student');
  isLoading = false;

  constructor(public userService: UserService, public toastr: ToastsManager){
  }

  newModel() {
    this.model = new RoleModel('','student');
  }

  submit() {
    this.isLoading = true;
    this.userService.changeUserRole(this.model).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    this.isLoading = false;
    var message = this.model.email + ' role changed to ' + this.model.role;
    this.toastr.success(message);
  }

  handleError(err) {
    this.isLoading = false;
    let data = err.json();
    this.newModel();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }
}
