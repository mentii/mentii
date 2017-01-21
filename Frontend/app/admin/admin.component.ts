import { Component } from '@angular/core';
import { RoleModel } from './role.model';
import { MentiiConfig } from '../mentii.config';
import { UserService } from '../user/user.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'admin-form',
  templateUrl: 'admin.html'
})

export class AdminComponent {
  model = new RoleModel('','student');
  mentiiConfig = new MentiiConfig();
  isLoading = false;

  constructor(public userService: UserService, public toastr: ToastsManager){
  }

  newModel() {
    this.model = new RoleModel('','student');
  }

  showChange(){
    console.log(this.model.role);
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
