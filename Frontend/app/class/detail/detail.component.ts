import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { ClassService } from '../class.service';
import { ToastrService } from 'ngx-toastr';
import { ClassModel } from '../class.model';
import { ModalDirective } from 'ng2-bootstrap';

@Component({
  moduleId: module.id,
  selector: 'class-detail',
  templateUrl: 'detail.html'
})

export class ClassDetailComponent implements OnInit, OnDestroy {
  model = new ClassModel('', '', '', '', '', [], []);
  private routeSub: any;
  showTeacherView = false;
  isLoading = true;
  @ViewChild('addActivityModal') public autoShownModal:ModalDirective;
  public isModalShown:boolean = false;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private classService: ClassService,
    private toastr: ToastrService
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
    this.isLoading = false;
  }

  handleError(err){
    this.toastr.error("Unable to access class.");
    this.router.navigateByUrl('/dashboard');
  }

  /* Modal Methods */
  public showCorrectionModal():void {
    this.isModalShown = true;
  }

  public hideCorrectionModal():void {
    this.autoShownModal.hide();
  }

  public onHidden():void {
    this.isModalShown = false;
  }

}
