import { Component, OnInit } from '@angular/core';
import { ClassModel } from '../class.model';
import { ClassService } from '../class.service';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router'


@Component({
  moduleId: module.id,
  selector: 'class-browse',
  templateUrl: 'browse.html'
})

export class ClassBrowseComponent implements OnInit {
  isLoading = true;
  classes: ClassModel[] = [];

  constructor(public classService: ClassService, public toastr: ToastrService, public router: Router ){
  }

  ngOnInit() {
    this.classService.getPublicClassList()
    .subscribe(
      data => this.handleInitSuccess(data.json()),
      err => this.handleInitError(err)
    );
  }

  handleInitSuccess(data) {
    this.isLoading = false;
    this.classes = data.payload.classes;
  }

  handleInitError(err) {
    this.isLoading = false;
    if (!err.isAuthenticationError) {
      this.toastr.error('The public class list failed to load.');
    }
  }
}
