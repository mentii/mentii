import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { ClassService } from '../class.service';
import { UserService } from '../../user/user.service';
import { ToastrService } from 'ngx-toastr';
import { ClassModel } from '../class.model';
import { NgForm } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'class-detail',
  templateUrl: 'detail.html'
})

export class ClassDetailComponent implements OnInit, OnDestroy {
  model = new ClassModel('', '', '', '', '', [], []);
  private routeSub: any;
  showTeacherView = false;
  isStudentInClass = false;
  isLoading = true;
  editMode = false;
  isJoinClassInprogress = false;
  isLeaveClassInProgress = false;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private classService: ClassService,
    private userService: UserService,
    private toastr: ToastrService
  ){}

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(qParams => {
      if(qParams['edit'] == 'true') {
        this.editMode = true;
      }
    });

    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.model.code = params['id'];
      this.classService.getClass(this.model.code)
      .subscribe(
        data => this.handleSuccess(data.json().payload.class),
        err => this.handleError(err)
      );
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  handleSuccess(data){
    this.model = new ClassModel(
      data.title,
      data.department,
      data.description,
      data.classSection,
      data.code,
      data.activities,
      data.students
    );
    this.showTeacherView = data.isTeacher || false;
    this.isStudentInClass = data.isStudent || false ;
    this.isLoading = false;
  }

  handleError(err){
    this.toastr.error("Unable to access class.");
    this.router.navigateByUrl('/dashboard');
  }

  toggleEditMode(){
    this.editMode = !this.editMode;
  }

  updateModel(form){
    this.model.title = form.value.title;
    this.model.department = form.value.department;
    this.model.section = form.value.section;
    this.model.description = form.value.description;
    this.toggleEditMode();
    this.toastr.success("Class successfully updated.");
  }

  handleUpdateError(err){
    this.toastr.error("Unable to update class details.");
  }

  saveChanges(form: NgForm){
    var newModel = new ClassModel(
      form.value.title,
      form.value.department,
      form.value.description,
      form.value.section,
      this.model.code,
      this.model.activities,
      this.model.students
    );

    this.classService.updateClassDetails(newModel)
      .subscribe(
        data => this.updateModel(form),
        err => this.handleUpdateError(err)
      );
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

  leaveClass(classCode) {
    this.isLeaveClassInProgress = true;
    this.userService.leaveClass(classCode)
    .subscribe(
      data => this.handleLeaveSuccess(data.json().payload),
      err => this.handleLeaveError(err)
    );
  }

  handleLeaveSuccess(json) {
    this.isLeaveClassInProgress = false;
    this.toastr.success('Successfully unenrolled');
    this.router.navigateByUrl('/dashboard');
  }

  handleLeaveError(err) {
    this.isLeaveClassInProgress = false;
    this.toastr.error('Unable to unenroll');
  }
}
