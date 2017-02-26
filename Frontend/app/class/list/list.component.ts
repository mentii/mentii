import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ToastrService } from 'ngx-toastr';
import { ClassService } from '../class.service';

@Component({
  moduleId: module.id,
  selector: 'class-list',
  templateUrl: 'list.html'
})

export class ClassListComponent implements OnInit {
  classes: ClassModel[] = [];
  isLoading = true;

  constructor(public classService: ClassService, public toastr: ToastrService){
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
    if (err.isAuthenticationError == false) {
      this.toastr.error("The class list component failed to load.");
    }
  }

}
