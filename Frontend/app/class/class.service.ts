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
    let getClassListUrl = this.mentiiConfig.getRootUrl() + '/user/classes/';
    let body = {}
    return this.authHttp.get(getClassListUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  getTaughtClassList():Observable<any> {
    let getTaughtClassListUrl = this.mentiiConfig.getRootUrl() + '/teacher/classes/';
    let body = {}
    return this.authHttp.get(getTaughtClassListUrl, body)
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

  addClass(classModel: ClassModel):Observable<any> {
    let createClassListUrl = this.mentiiConfig.getRootUrl() + '/class';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers })
    let body = {
      "title": classModel.title,
      "department": classModel.department,
      "description": classModel.description,
      "section": classModel.section
    }
    return this.authHttp.post(createClassListUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }
}
