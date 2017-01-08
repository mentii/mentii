import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'class-detail',
  templateUrl: 'detail.html'
})

export class ClassDetailComponent implements OnInit, OnDestroy {
  classCode: String;
  private routeSub: any;

  constructor(private activatedRoute: ActivatedRoute){
  }

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
       this.classCode = params['id'];
       // TODO: dispatch action to load the details based off of class code here.
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

}
