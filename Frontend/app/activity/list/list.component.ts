import { Component, Input } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../../user/user.service';

@Component({
  moduleId: module.id,
  selector: 'activity-list',
  templateUrl: 'list.html'
})

export class ActivityListComponent {
  @Input() activities;
  @Input() classCode;
  @Input() isStudentInClass;
  @Input() isTeacher;
  isJoinClassInprogress = false;

  constructor(public toastr: ToastrService, public userService: UserService ){
  }

  joinClass(classCode) {
    this.isJoinClassInprogress = true;
    this.userService.joinClass(classCode)
    .subscribe(
      data => this.handleJoinSuccess(data.json().payload),
      err => this.handleJoinError(err)
    );
  }

  handleJoinSuccess(json) {
    this.toastr.success('You have joined ' + json.title);
    this.isJoinClassInprogress = false;
    this.isStudentInClass = true;
  }

  handleJoinError(err) {
    this.isJoinClassInprogress = false;
    this.toastr.error('Unable to join class');
  }
}
