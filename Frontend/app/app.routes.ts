// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { RegistrationComponent } from './registration/registration.component';

// Route Configuration
export const routes: Routes = [
  { path: 'registration', component: RegistrationComponent }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
