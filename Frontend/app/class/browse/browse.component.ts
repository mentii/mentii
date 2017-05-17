import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router'
import { UserService } from '../../user/user.service';
import { AuthHttp } from '../../utils/AuthHttp.service';


@Component({
  moduleId: module.id,
  selector: 'class-browse',
  templateUrl: 'browse.html'
})

export class ClassBrowseComponent implements OnInit {
  isLoading = true;
  isJoiningClass = false;
  classes: ClassModel[] = [];
  taughtClasses: ClassModel[] = [];
  classCode = "";

  constructor(
    public classService: ClassService,
    public toastr: ToastrService,
    public router: Router,
    public userService: UserService,
    private authHttp: AuthHttp
    ){}

  ngOnInit() {
    this.classService.getPublicClassList()
    .subscribe(
      data => this.handleInitSuccess(data.json()),
      err => this.handleInitError(err)
    );
  }

  handleInitSuccess(data) {
    this.classes = data.payload.classes;
    if(this.authHttp.loadRole() == 'teacher' || this.authHttp.loadRole() == 'admin'){
      this.classService.getTaughtClassList()
      .subscribe(
        data => this.handleTaughtSuccess(data.json()),
        err => this.handleTaughtError(err)
      );
    } else {
      this.isLoading = false;
    }
  }

  handleInitError(err) {
    if (!err.isAuthenticationError) {
      this.toastr.error('The public class list failed to load.');
    }
    this.isLoading = false;
  }

  handleTaughtSuccess(data){
    this.taughtClasses = data.payload.classes;
    // remove taught classes from classes array
    for(let i=0; i < this.taughtClasses.length; i++) {
      for(let k=0; k < this.classes.length; k++) {
        if(this.classes[k].code == this.taughtClasses[i].code){
          this.classes.splice(k,1);
        }
      }
    }
    this.isLoading = false;
  }

  handleTaughtError(err){
    if (err.isAuthenticationError == false) {
      this.toastr.error("The taught class list failed to load.");
    }
    this.isLoading = false;
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
