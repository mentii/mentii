import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ClassService } from '../class.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'class-detail',
  templateUrl: 'detail.html'
})

export class ClassDetailComponent implements OnInit, OnDestroy {
  classCode: String;
  private routeSub: any;

  constructor(private activatedRoute: ActivatedRoute, public classService: ClassService, public toastr: ToastsManager){
  }

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.classCode = params['id'];
      this.classService.getClass(this.classCode)
      .subscribe(
        data => this.handleSuccess(data.json()),
        err => this.handleError(err)
      );
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  handleSuccess(data){
  }

  handleError(err){
  }

}
