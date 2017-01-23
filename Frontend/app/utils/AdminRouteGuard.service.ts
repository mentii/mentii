import { CanActivate } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthHttp } from './AuthHttp.service';
import { Router } from '@angular/router';

@Injectable()
export class AdminRouteGuard implements CanActivate {

  constructor(private authHttpService: AuthHttp, private router: Router) {}

  canActivate() {
    let role = this.authHttpService.propagateRole();
    if (role != 'admin') {
      //by rerouting will not hit the return true
      this.router.navigateByUrl('/dashboard');
    }
    return true;
  }
}
