/* Angular Builtins */
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CoreModule } from './core.module';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule, RequestOptions, XHRBackend } from '@angular/http';
import { Router } from '@angular/router';
/* App Config */
import { routing } from './app.routes';
/* Services */
import { UserService } from './user/user.service';
import { ClassService } from './class/class.service';
import { ProblemService } from './problem/problem.service';
import { ToastModule } from 'ng2-toastr/ng2-toastr';
import { BookService } from './book/book.service';
/* Components */
import { AdminComponent } from './admin/admin.component';
import { AppComponent } from './app.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { SigninComponent } from './user/signin/signin.component';
import { RootComponent } from './root/root.component';
import { DashboardComponent } from './root/dashboard.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
import { SecureTestComponent } from './secureTest/secureTest.component';
import { ClassListComponent } from './class/list/list.component';
import { TaughtClassListComponent } from './class/taughtList/taughtList.component';
import { ClassDetailComponent } from './class/detail/detail.component';
import { CreateClassComponent } from './class/create/create.component';
import { ClassBrowseComponent } from './class/browse/browse.component';
import { ClassListItemComponent } from './class/listItem/classListItem.component';
import { ActivityListComponent } from './activity/list/list.component';
import { DisplayProblemComponent } from './problem/display/displayProblem.component';
import { UserListComponent } from './user/list/list.component';
import { ChangeRole } from './admin/changeRole/changeRole.component'
import { CreateBookComponent } from './book/create/createBook.component';
import { ChapterListComponent } from './book/chapterList/chapterList.component';
import { ChapterListItemComponent } from './book/chapterList/chapterListItem.component';
/* Directives */
import { EqualValidator } from './directives/equal-validator.directive';
import { DeleteValue } from './directives/delete-value-validator.directive';
import { ClearPlaceholder } from './directives/clearPlaceholderOnFocus.directive';
/* Route Guards */
import { AuthRouteGuard } from './utils/AuthRouteGuard.service';
import { TeacherRouteGuard } from './utils/TeacherRouteGuard.service';
import { AdminRouteGuard } from './utils/AdminRouteGuard.service';
/* Vendor */
import { LaddaModule } from 'angular2-ladda';

@NgModule({

  imports:      [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    ToastModule,
    LaddaModule.forRoot({style: "zoom-in"}),
    routing,
    CommonModule,
    CoreModule
  ],

  declarations: [
    AdminComponent,
    ActivityListComponent,
    DisplayProblemComponent,
    AppComponent,
    RegistrationComponent,
    RootComponent,
    DashboardComponent,
    PageNotFoundComponent,
    SecureTestComponent,
    EqualValidator,
    DeleteValue,
    SigninComponent,
    ClassListComponent,
    ClassDetailComponent,
    CreateClassComponent,
    ClassBrowseComponent,
    ClassListItemComponent,
    TaughtClassListComponent,
    ClearPlaceholder,
    UserListComponent,
    ChangeRole,
    CreateBookComponent,
    ChapterListComponent,
    ChapterListItemComponent
  ],

  providers:  [
    UserService,
    ClassService,
    ProblemService,
    AuthRouteGuard,
    TeacherRouteGuard,
    AdminRouteGuard,
    BookService
  ],

  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
