// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { RootComponent } from './root/root.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
import { SecureTestComponent } from './secureTest/secureTest.component';
import { ClassDetailComponent } from './class/detail/detail.component';
import { CreateClassComponent } from './class/create/create.component';

// Route Configuration
export const routes: Routes = [
  { path: '', component: RootComponent }, // Application root
  { path: 'register', component: RegistrationComponent },
  { path: 'secure-test', component: SecureTestComponent },
  { path: 'class/:id', component: ClassDetailComponent },
  { path: 'create/class', component: CreateClassComponent },

  // The PageNotFound route MUST be last in this list
  { path: '**', component: PageNotFoundComponent } // Page Not Found
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
