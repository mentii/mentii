// ====== ./app/app.component.ts ======
import { Component } from '@angular/core';
// Import router directives
// Deprecated
// import { ROUTER_DIRECTIVES } from '@angular/router';

@Component({
  selector: 'my-app',
  template: `

            <a [routerLink]="['/']">Home</a>
            <a [routerLink]="['/registration']">Register</a>


    <!-- Router Outlet -->
    <router-outlet></router-outlet>
  `,
  // Not necessary as we have provided directives using
  // `RouterModule` to root module
  // Tell component to use router directives
  // directives: [ROUTER_DIRECTIVES]
})

// App Component class
export class AppComponent {}
