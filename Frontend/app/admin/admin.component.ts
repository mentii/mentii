import { Component } from '@angular/core';
import { RoleModel } from './role.model';
import { UserService } from '../user/user.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  moduleId: module.id,
  selector: 'admin-form',
  templateUrl: 'admin.html'
})

export class AdminComponent {
  model = new RoleModel('','student');
  isLoading = false;

  constructor(public userService: UserService, public toastr: ToastrService){
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
