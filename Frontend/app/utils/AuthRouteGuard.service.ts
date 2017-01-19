import { CanActivate } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthHttp } from './AuthHttp.service';
import { Router } from '@angular/router';

@Injectable()
export class AuthRouteGuard implements CanActivate {

  constructor(private authHttpService: AuthHttp, private router: Router) {}

  canActivate() {
    let authStatus: boolean = this.authHttpService.checkAuthStatus();
    if (authStatus === false) {
      // Return to sign in if not authenticated
      this.router.navigateByUrl('/sign-in');
    }
    return authStatus;
  }
}
