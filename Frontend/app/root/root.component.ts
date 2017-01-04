import { Component } from '@angular/core';
import { SigninComponent } from '../user/signin/signin.component'
import { AuthHttp } from '../utils/AuthHttp.service';

@Component({
  moduleId: module.id,
  selector: 'root',
  templateUrl: 'root.html'
})
export class RootComponent {
  isUserAuthenticated = false;

  constructor( public authHttp: AuthHttp){
    this.checkAuthToken();
  }

  checkAuthToken() {
    if (this.authHttp.loadAuthToken() == null) {
      this.isUserAuthenticated = false;
    } else {
      this.isUserAuthenticated = true;
    }
  }
}
