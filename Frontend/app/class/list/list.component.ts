import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ClassModel } from '../class.model';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { ClassService } from '../class.service';

@Component({
  moduleId: module.id,
  selector: 'class-list',
  templateUrl: 'list.html'
})

export class ClassListComponent implements OnInit {
  classes: ClassModel[];
  isLoading = true;

  constructor(public classService: ClassService, public router: Router, public toastr: ToastsManager){
  }

  ngOnInit() {
    this.classService.getClassList()
    .subscribe(
      data => this.handleSuccess(data.json()),
      err => this.handleError(err)
    );
  }

  handleSuccess(data){
    this.isLoading = false;
    this.classes = data.payload.classes;
  }

  handleError(err){
    this.isLoading = false;
    this.toastr.error("The class list failed to load.");
  }

}
