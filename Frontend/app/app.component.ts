// ====== ./app/app.component.ts ======
import { Component, ViewContainerRef, OnInit } from '@angular/core';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { AuthHttp } from './utils/AuthHttp.service';
import { Router } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: 'app.template.html',
})

// App Component class
export class AppComponent implements OnInit {
  // Default to false
  isAuthenticated = false;

  constructor(public toastr: ToastsManager, public authHttpService: AuthHttp, public router: Router, vRef: ViewContainerRef) {
    this.toastr.setRootViewContainerRef(vRef);
  }

  ngOnInit() {
    // Check for updates on the isAuthenticated property of AuthHttp
    this.authHttpService.isAuthenticated$.subscribe(
      data => {
        // data is true/false
        this.isAuthenticated = data;
      });

      // Initialize the check on authentication.
      // Used mostly when opening the app to a weird page such as /class directly
      this.authHttpService.checkAuthStatus();
  }

  logout() {
    this.authHttpService.logout();
    // Return to sign in page
    this.router.navigateByUrl('');
  }
}
