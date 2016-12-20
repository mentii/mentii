import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule, RequestOptions, XHRBackend } from '@angular/http';
import { AuthHttp } from './utils/AuthHttp.service';
import { FormsModule }   from '@angular/forms';
import { AppComponent } from './app.component';
import { RegistrationComponent }   from './registration/registration.component';
import { RootComponent }   from './root/root.component';
import { PageNotFoundComponent }   from './pageNotFound/pageNotFound.component';
import { SecureTestComponent }   from './secure-test/secure-test.component';
import { routing } from './app.routes';
import {Router} from '@angular/router';
import { EqualValidator } from './directives/equal-validator.directive';
import { DeleteValue } from './directives/delete-value-validator.directive';

@NgModule({
  imports:      [ BrowserModule, FormsModule, HttpModule, routing],
  declarations: [ AppComponent, RegistrationComponent, RootComponent, PageNotFoundComponent, SecureTestComponent, EqualValidator, DeleteValue],
  providers: [
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
