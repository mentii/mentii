import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'class-browse',
  templateUrl: 'browse.html'
})

export class ClassBrowseComponent implements OnInit {
  isLoading = true;
  classes: ClassModel[] = [];

  constructor(public classService: ClassService, public toastr: ToastsManager){
  }

  ngOnInit() {
    this.classService.getPublicClassList()
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
    if (!err.isAuthenticationError) {
      this.toastr.error("The public class list failed to load.");
    }
  }

  joinClass() {
    alert("not implemented");
  }
}
