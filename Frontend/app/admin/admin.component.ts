import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../user/user.service';

@Component({
  moduleId: module.id,
  selector: 'admin-form',
  templateUrl: 'admin.html'
})

export class AdminComponent {
  private routeSub: any;
  activeControl = '';

  constructor(private activatedRoute: ActivatedRoute){
  }

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      if (params['control']) {
        this.activeControl = params['control'];
      }
    });
  }
}