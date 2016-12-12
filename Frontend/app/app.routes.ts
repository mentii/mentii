// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { RootComponent } from './root/root.component';
import { RegistrationComponent } from './registration/registration.component';

// Route Configuration
export const routes: Routes = [
  { path: '', component: RootComponent }, // Application root
  { path: 'register', component: RegistrationComponent }
  // { path: '**', component: PageNotFoundComponent } // TODO: Page Not Found
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
