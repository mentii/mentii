// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { RootComponent } from './root/root.component';
import { RegistrationComponent } from './registration/registration.component';

// Route Configuration
export const routes: Routes = [
  { path: '', component: RootComponent },
  { path: 'register', component: RegistrationComponent }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
