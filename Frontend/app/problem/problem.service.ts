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

@Injectable()
export class ProblemService {
  mentiiConfig = new MentiiConfig();

  constructor (private authHttp: AuthHttp) {
  }

  getProblemSteps(classCode, activityCode): Observable<any> {
    let getUrl = this.mentiiConfig.getRootUrl() + '/problem/' + classCode + '/' + activityCode + '/';
    let body = {}
    return this.authHttp.get(getUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }
  
  postProblemSuccess(classCode, activityCode, problemIndex, wasSuccessful): Observable<any> {
    let postUrl = this.mentiiConfig.getRootUrl() + '/problem/' + classCode + '/' + activityCode + '/';
    let body = {"problemIndex": problemIndex, "didSucceed": wasSuccessful}
    return this.authHttp.post(postUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }
  
}
