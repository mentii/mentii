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
  role;

  constructor(public toastr: ToastsManager, public authHttpService: AuthHttp, public router: Router, vRef: ViewContainerRef) {
    this.toastr.setRootViewContainerRef(vRef);
  }

  ngOnInit() {
    // Check for updates on the isAuthenticated property of AuthHttp
    this.authHttpService.isAuthenticated$.subscribe(
      data => {
        // data is true/false
        this.isAuthenticated = data;
      }
    );

    // Check for updates on the role of the user from AuthHttp
    this.authHttpService.role$.subscribe(
      data => {
        // data is a string of the users role
        this.role = data;
      }
    );
    
    // Initialize the check on the role and authentication
    // Used mostly when opening the app to a weird page such as /create/class directly
    this.authHttpService.propagateRole();
    this.authHttpService.propagateAuthStatus();
  }

  logout() {
    this.authHttpService.logout();
    // Return to sign in page
    this.router.navigateByUrl('');
  }
}
