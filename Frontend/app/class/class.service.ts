// Builtin
import { Injectable } from '@angular/core';
import { Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { NgForm } from '@angular/forms';

// Services
import { AuthHttp } from '../utils/AuthHttp.service';
// Utilities
import { MentiiConfig } from '../mentii.config';
// Models
import { ClassModel } from './class.model';
import { ActivityModel } from '../activity/activity.model';

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

  getClass(classCode:String):Observable<any> {
    let getClassUrl = this.mentiiConfig.getRootUrl() + '/classes/' + classCode;
    let body = {}
    return this.authHttp.get(getClassUrl, body)
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

  removeStudentFromClass(email:string, classCode:string):Observable<any> {
    let removeStudentUrl = this.mentiiConfig.getRootUrl() + '/classes/remove';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers })
    let body = {
      'email': email,
      'classCode': classCode
    }
    return this.authHttp.post(removeStudentUrl, body, options)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  updateClassDetails(classModel: ClassModel):Observable<any> {
    let updateClassDetailsUrl = this.mentiiConfig.getRootUrl() + '/class/details/update';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers })
    let body = {
      'title': classModel.title,
      'department': classModel.department,
      'description': classModel.description,
      'section': classModel.section,
      'code': classModel.code
    }
    return this.authHttp.post(updateClassDetailsUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  addActivity(classCode: string, newActivity: ActivityModel):Observable<any> {
    let addActivityUrl = this.mentiiConfig.getRootUrl() + '/class/'+classCode+'/activities';
    let body = {
      'title': newActivity.title,
      'description' : newActivity.description,
      'problemCount' : newActivity.problemCount,
      'startDate': newActivity.startDate,
      'dueDate': newActivity.dueDate,
      'bookId': newActivity.bookId,
      'chapterTitle': newActivity.chapterTitle,
      'sectionTitle': newActivity.sectionTitle
    }
    return this.authHttp.post(addActivityUrl, body)
      .map((res:Response) => res)
      .catch((error:any) => Observable.throw(error));
  }
}
