// ====== ./app/app.routes.ts ======

// Imports
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ActivationComponent } from './user/activation/activation.component';
import { AdminComponent } from './admin/admin.component';
import { AppComponent } from './app.component';
import { RootComponent } from './root/root.component';
import { DashboardComponent } from './root/dashboard.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { ForgotPasswordComponent } from './user/forgotPassword/forgotPassword.component';
import { ResetPasswordComponent } from './user/resetPassword/resetPassword.component';
import { SigninComponent } from './user/signin/signin.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
import { ClassListComponent } from './class/list/list.component';
import { ClassDetailComponent } from './class/detail/detail.component';
import { CreateClassComponent } from './class/create/create.component';
import { ClassBrowseComponent } from './class/browse/browse.component';
import { DisplayProblemComponent } from './problem/display/displayProblem.component';

// Route Guards
import { AuthRouteGuard } from './utils/AuthRouteGuard.service';
import { TeacherRouteGuard } from './utils/TeacherRouteGuard.service';
import { AdminRouteGuard } from './utils/AdminRouteGuard.service';

// Route Configuration
export const routes: Routes = [
  { path: '', component: RootComponent }, // Application root
  { path: 'sign-in', component: SigninComponent },
  { path: 'register', component: RegistrationComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'reset-password/:id', component: ResetPasswordComponent },
  { path: 'activation/:id', component: ActivationComponent},
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthRouteGuard] },
  { path: 'class/:id', component: ClassDetailComponent, canActivate: [AuthRouteGuard] },
  { path: 'class', component: ClassBrowseComponent, canActivate: [AuthRouteGuard] },
  { path: 'admin/:control', component: AdminComponent, canActivate: [AuthRouteGuard, AdminRouteGuard]},
  { path: 'admin', component: AdminComponent, canActivate: [AuthRouteGuard, AdminRouteGuard]},
  { path: 'create/class', component: CreateClassComponent, canActivate: [AuthRouteGuard, TeacherRouteGuard] },
  { path: 'problem/display/:classCode/:problemCode', component: DisplayProblemComponent, canActivate: [AuthRouteGuard] },

  // The PageNotFound route MUST be last in this list
  { path: '**', component: PageNotFoundComponent } // Page Not Found
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
