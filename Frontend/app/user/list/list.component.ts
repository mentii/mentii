import { Component, Input } from '@angular/core';
import { ClassService } from '../../class/class.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  moduleId: module.id,
  selector: 'user-list',
  templateUrl: 'list.html'
})

export class UserListComponent {
  @Input('users') users;
  @Input('classCode') classCode;

  private selected:string;

  constructor(private classService: ClassService, private toastr: ToastrService){}

  selectedUser(user:string){
  	this.selected = user;
  }

  removeUser(){
    this.classService.removeStudentFromClass(this.selected, this.classCode)
      .subscribe(
        data => this.handleSuccess(),
        err => this.handleError(err)
    );
  }

  handleSuccess(){
    var message = this.selected + ' was succesfully removed.'
    this.toastr.success(message);

    // remove user from list
    let index = this.users.indexOf(this.selected);
    this.users.splice(index,1);

    //send email
  }

  handleError(err){
    let message = 'Unable to remove ' + this.selected + ' from class.'
    this.toastr.error(message)
  }
}
