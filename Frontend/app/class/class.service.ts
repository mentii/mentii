// Builtin
import { Injectable } from '@angular/core';
import { Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
// Services
import { AuthHttp } from '../utils/AuthHttp.service'
// Utilities
import { MentiiConfig } from '../mentii.config'
// Models
import { ClassModel } from './class.model';

@Injectable()
export class ClassService {
  mentiiConfig = new MentiiConfig();

  constructor (private authHttp: AuthHttp) {
  }

  getClassList():Observable<any> {
    let getClassListUrl = this.mentiiConfig.getRootUrl() + '/class-list/';
    let body = {}
    return this.authHttp.get(getClassListUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  getPublicClassList(): Observable<any> {
      let getClassListUrl = this.mentiiConfig.getRootUrl() + '/classes/';
      let body = {}
      return this.authHttp.get(getClassListUrl, body)
      .map((res:Response) => res)
      .catch((error:any) => Observable.throw(error));
  }
}
