import { Component } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'class-create',
  templateUrl: 'create.html'
})

export class CreateClassComponent {
  model = new ClassModel('', '', '', '', '');
  isLoading = false;
  classCreated = false;

  constructor(public classService: ClassService, public toastr: ToastsManager){
  }

  newModel() {
    this.model = new ClassModel('', '', '', '', '');
  }

  submit() {
    this.isLoading = true;
    this.classService.addClass(this.model).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    this.isLoading = false;
    this.classCreated = true;
    var message = this.model.title + ' Class Created'
    this.toastr.success(message);
    this.newModel();
  }

  handleError(err) {
    this.isLoading = false;
    this.newModel();
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }
}
