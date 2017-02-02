import { Component, OnInit } from '@angular/core';
import { AuthHttp } from '../utils/AuthHttp.service';

@Component({
  moduleId: module.id,
  selector: 'dashboard',
  templateUrl: 'dashboard.html'
})

export class DashboardComponent implements OnInit {
  role;

  constructor(public authHttpService: AuthHttp){
  }

  ngOnInit() {
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
  }

}
