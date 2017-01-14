import { Component } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'class-browse',
  templateUrl: 'browse.html'
})

export class ClassBrowseComponent {
  isLoading = true;
  classes: ClassModel[] = [];

  constructor(public classService: ClassService, public toastr: ToastsManager){
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
    this.toastr.error("The class list failed to load.");
  }

  joinClass() {
    alert("not implemented");
  }

}
