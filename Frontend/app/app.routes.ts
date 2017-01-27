// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AdminComponent } from './admin/admin.component';
import { AppComponent } from './app.component';
import { RootComponent } from './root/root.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { SigninComponent } from './user/signin/signin.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
import { SecureTestComponent } from './secureTest/secureTest.component';
import { ClassListComponent } from './class/list/list.component';
import { ClassDetailComponent } from './class/detail/detail.component';
import { CreateClassComponent } from './class/create/create.component';
import { ClassBrowseComponent } from './class/browse/browse.component';

// Route Guards
import { AuthRouteGuard } from './utils/AuthRouteGuard.service';
import { TeacherRouteGuard } from './utils/TeacherRouteGuard.service';
import { AdminRouteGuard } from './utils/AdminRouteGuard.service';

// Route Configuration
export const routes: Routes = [
  { path: '', component: RootComponent }, // Application root
  { path: 'sign-in', component: SigninComponent },
  { path: 'register', component: RegistrationComponent },
  { path: 'secure-test', component: SecureTestComponent, canActivate: [AuthRouteGuard] },
  { path: 'dashboard', component: ClassListComponent, canActivate: [AuthRouteGuard] },
  { path: 'class', component: ClassBrowseComponent, canActivate: [AuthRouteGuard] },
  { path: 'class/:id', component: ClassDetailComponent, canActivate: [AuthRouteGuard] },
  { path: 'admin', component: AdminComponent, canActivate: [AuthRouteGuard, AdminRouteGuard]},
  { path: 'create/class', component: CreateClassComponent, canActivate: [AuthRouteGuard, TeacherRouteGuard] },

  // The PageNotFound route MUST be last in this list
  { path: '**', component: PageNotFoundComponent } // Page Not Found
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
