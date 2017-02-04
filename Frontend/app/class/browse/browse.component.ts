import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { UserService } from '../../user/user.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { Router } from '@angular/router'


@Component({
  moduleId: module.id,
  selector: 'class-browse',
  templateUrl: 'browse.html'
})

export class ClassBrowseComponent implements OnInit {
  isLoading = true;
  classes: ClassModel[] = [];
  isJoinClassInprogress = false;

  constructor(public classService: ClassService, public toastr: ToastsManager, public router: Router, public userService: UserService ){
  }

  ngOnInit() {
    this.classService.getPublicClassList()
    .subscribe(
      data => this.handleInitSuccess(data.json()),
      err => this.handleInitError(err)
    );
  }

  handleInitSuccess(data) {
    this.isLoading = false;
    this.classes = data.payload.classes;
  }

  handleInitError(err) {
    this.isLoading = false;
    if (!err.isAuthenticationError) {
      this.toastr.error('The public class list failed to load.');
    }
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
