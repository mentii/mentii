import { Component } from '@angular/core';
import { ClassModel } from '../class.model';
import { Router } from '@angular/router';
import { ClassService } from '../class.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  moduleId: module.id,
  selector: 'class-create',
  templateUrl: 'create.html'
})

export class CreateClassComponent {
  model = new ClassModel('', '', '', '', '', [], []);
  isLoading = false;

  constructor(public classService: ClassService, public toastr: ToastrService, public router: Router){
  }

  submit() {
    this.isLoading = true;
    this.classService.addClass(this.model).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    var message = this.model.title + ' Class Created'
    this.toastr.success(message);
    this.router.navigateByUrl('/dashboard');
  }

  handleError(err) {
    this.isLoading = false;
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }
}
