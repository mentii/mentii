// ====== ./app/app.component.ts ======
import { Component } from '@angular/core';
// Import router directives
// Deprecated
// import { ROUTER_DIRECTIVES } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: 'app.template.html',
  // Not necessary as we have provided directives using
  // `RouterModule` to root module
  // Tell component to use router directives
  // directives: [ROUTER_DIRECTIVES]
})

// App Component class
export class AppComponent {}
