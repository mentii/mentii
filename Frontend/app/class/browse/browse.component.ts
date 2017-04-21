import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router'
import { UserService } from '../../user/user.service';


@Component({
  moduleId: module.id,
  selector: 'class-browse',
  templateUrl: 'browse.html'
})

export class ClassBrowseComponent implements OnInit {
  isLoading = true;
  isJoiningClass = false;
  classes: ClassModel[] = [];
  classCode = "";

  constructor(public classService: ClassService, public toastr: ToastrService, public router: Router, public userService: UserService ){}

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

  submit() {
    this.isJoiningClass = true;
    this.userService.joinClass(this.classCode)
      .subscribe(
        data => this.handleJoinSuccess(data.json().payload),
        err => this.handleJoinError(err)
    );
  }

  handleJoinSuccess(json) {
    this.isJoiningClass = false;
    this.toastr.success('You have joined ' + json.title);
    this.router.navigateByUrl('/class/' + json.code);
  }

  handleJoinError(err) {
    this.isJoiningClass = false;
    this.toastr.error('Unable to join class');
  }
}
