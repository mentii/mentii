import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { ClassService } from '../class.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { ClassModel } from '../class.model';

@Component({
  moduleId: module.id,
  selector: 'class-detail',
  templateUrl: 'detail.html'
})

export class ClassDetailComponent implements OnInit, OnDestroy {
  model = new ClassModel('', '', '', '', '', [], []);
  private routeSub: any;
  showTeacherView = false;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private classService: ClassService,
    private toastr: ToastsManager
  ){}

  ngOnInit() {
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
      data.section,
      data.code,
      data.activities,
      data.students
    );
    this.showTeacherView = data.isTeacher;
  }

  handleError(err){
    this.toastr.error("Unable to access class.");
    this.router.navigateByUrl('/dashboard');
  }

}
