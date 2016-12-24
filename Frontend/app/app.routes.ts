// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { RootComponent } from './root/root.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
import { SecureTestComponent } from './secureTest/secureTest.component';

// Route Configuration
export const routes: Routes = [
  { path: '', component: RootComponent }, // Application root
  { path: 'register', component: RegistrationComponent },
  { path: 'secure-test', component: SecureTestComponent },

  // The PageNotFound route MUST be last in this list
  { path: '**', component: PageNotFoundComponent } // Page Not Found
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
