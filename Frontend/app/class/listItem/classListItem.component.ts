import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../../user/user.service';

@Component({
  moduleId: module.id,
  selector: 'class-list-item',
  templateUrl: 'classListItem.html'
})

export class ClassListItemComponent {
  @Input() classObject;
  @Input() classDetailsButton;
  @Input() joinClassButtonShown;
  @Input() editClassButtonShown;
  isJoinClassInprogress = false;
  isLeaveClassInProgress = false;

  constructor(public toastr: ToastrService, public router: Router, public userService: UserService ){
  }

  joinClass(classCode) {
    this.isJoinClassInprogress = true;
    this.userService.joinClass(classCode)
    .subscribe(
      data => this.handleJoinSuccess(data.json().payload),
      err => this.handleJoinError(err)
    );
  }

  leaveClass(classCode) {
    this.isLeaveClassInProgress = true;
    this.userService.leaveClass(classCode)
    .subscribe(
      data => this.handleLeaveSuccess(data.json().payload),
      err => this.handleLeaveError(err)
    );
  }

  handleJoinSuccess(json) {
    this.isJoinClassInprogress = false;
    this.toastr.success('You have joined ' + json.title);
    this.router.navigateByUrl('/class/' + json.code);
  }

  handleJoinError(err) {
    this.isJoinClassInprogress = false;
    this.toastr.error('Unable to join class');
  }

  handleLeaveSuccess(json) {
    this.isLeaveClassInProgress = false;
    this.toastr.success('You have left ' + json.title);
    this.router.navigateByUrl('/dashboard');
  }

  handleLeaveError(err) {
    this.isLeaveClassInProgress = false;
    this.toastr.error('Unable to leave class');
  }
}
