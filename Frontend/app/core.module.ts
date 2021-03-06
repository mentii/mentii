import { NgModule } from '@angular/core';
import { HttpModule, RequestOptions, XHRBackend } from '@angular/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ToastrService } from 'ngx-toastr';
import { AuthHttp } from './utils/AuthHttp.service';

/*
Things imported in this module are singletons for the entire app
 */
@NgModule({
  imports: [
    CommonModule
  ],
  exports: [ ],
  declarations: [ ],
  providers: [
    {
      provide: AuthHttp,
      useFactory: (backend: XHRBackend, options: RequestOptions, router: Router, toastr: ToastrService) => {
        return new AuthHttp(backend, options, router, toastr);
      },
      deps: [XHRBackend, RequestOptions, Router, ToastrService]
    }
  ]
})
export class CoreModule { }
