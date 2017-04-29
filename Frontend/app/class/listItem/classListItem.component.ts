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

  handleJoinSuccess(json) {
    this.toastr.success('You have joined ' + json.title);
    this.router.navigateByUrl('/class/' + json.code);
  }

  handleJoinError(err) {
    this.isJoinClassInprogress = false;
    this.toastr.error('Unable to join class');
  }
}
