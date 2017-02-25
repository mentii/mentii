import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { ClassService } from '../class.service';

@Component({
  moduleId: module.id,
  selector: 'taught-list',
  templateUrl: 'taughtList.html'
})

export class TaughtClassListComponent implements OnInit {
  classes: ClassModel[] = [];
  isLoading = true;

  constructor(public classService: ClassService, public toastr: ToastsManager){
  }

  ngOnInit() {
    this.classService.getTaughtClassList()
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
      this.toastr.error("The taught class list failed to load.");
    }
  }

}
