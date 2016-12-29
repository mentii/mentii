/* Angular Builtins */
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule, RequestOptions, XHRBackend } from '@angular/http';
import { Router } from '@angular/router';
/* App Config */
import { routing } from './app.routes';
/* Services */
import { AuthHttp } from './utils/AuthHttp.service';
import { UserService } from './user/user.service';
import { ToastModule } from 'ng2-toastr/ng2-toastr';
/* Components */
import { AppComponent } from './app.component';
import { RegistrationComponent } from './user/registration/registration.component';
import { SigninComponent } from './user/signin/signin.component';
import { RootComponent } from './root/root.component';
import { PageNotFoundComponent } from './pageNotFound/pageNotFound.component';
import { SecureTestComponent } from './secureTest/secureTest.component';
/* Directives */
import { EqualValidator } from './directives/equal-validator.directive';
import { DeleteValue } from './directives/delete-value-validator.directive';

@NgModule({
  imports:      [ BrowserModule, FormsModule, HttpModule, ToastModule, routing],
  declarations: [ AppComponent, RegistrationComponent, RootComponent, PageNotFoundComponent, SecureTestComponent, EqualValidator, DeleteValue, SigninComponent],
  providers: [UserService,
    {
      provide: AuthHttp,
      useFactory: (backend: XHRBackend, options: RequestOptions, router: Router) => {
        return new AuthHttp(backend, options, router);
      },
      deps: [XHRBackend, RequestOptions, Router]
    }
  ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
