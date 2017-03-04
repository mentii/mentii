import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  moduleId: module.id,
  selector: 'activation-page',
  templateUrl: 'activation.html'
})

export class ActivationComponent implements OnInit, OnDestroy {
  activationSuccessful = false;
  isLoading = false;
  private routeSub: any;

  constructor(
    private userService: UserService,
    private activatedRoute: ActivatedRoute
  ){}

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.activate(params['id']);
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  activate(activationId) {
    this.isLoading = true;
    this.userService.activation(activationId).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    this.isLoading = false;
    this.activationSuccessful = true;
  }

  handleError(err) {
    this.isLoading = false;
  }
}
