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
import { ToastrModule } from 'ngx-toastr';
import { ProblemService } from './problem/problem.service';
import { BookService } from './book/book.service';
/* Components */
import { ActivationComponent } from './user/activation/activation.component';
import { AdminComponent } from './admin/admin.component';
import { AppComponent } from './app.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { ForgotPasswordComponent } from './user/forgotPassword/forgotPassword.component';
import { SigninComponent } from './user/signin/signin.component';
import { RootComponent } from './root/root.component';
import { DashboardComponent } from './root/dashboard.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
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
import { SectionListComponent } from './book/sectionList/sectionList.component';
import { SectionListItemComponent } from './book/sectionList/sectionListItem.component';
import { ProblemListComponent } from './book/problemList/problemList.component';
import { ProblemListItemComponent } from './book/problemList/problemListItem.component';
/* Directives */
import { EqualValidator } from './directives/equal-validator.directive';
import { DeleteValue } from './directives/delete-value-validator.directive';
import { ClearPlaceholder } from './directives/clearPlaceholderOnFocus.directive';
import { HideNgInvalid } from './directives/hideNgInvalid.directive';
/* Route Guards */
import { AuthRouteGuard } from './utils/AuthRouteGuard.service';
import { TeacherRouteGuard } from './utils/TeacherRouteGuard.service';
import { AdminRouteGuard } from './utils/AdminRouteGuard.service';
/* Vendor */
import { LaddaModule } from 'angular2-ladda';
import { ModalModule } from 'ng2-bootstrap';

@NgModule({

  imports:      [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    ToastrModule.forRoot({preventDuplicates: true}),
    LaddaModule.forRoot({style: "zoom-in"}),
    [ModalModule.forRoot()],
    routing,
    CommonModule,
    CoreModule
  ],

  declarations: [
    ActivationComponent,
    AdminComponent,
    ActivityListComponent,
    DisplayProblemComponent,
    AppComponent,
    RegistrationComponent,
    ForgotPasswordComponent,
    RootComponent,
    DashboardComponent,
    PageNotFoundComponent,
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
    ChapterListItemComponent,
    SectionListComponent,
    SectionListItemComponent,
    ProblemListComponent,
    ProblemListItemComponent,
    HideNgInvalid
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
