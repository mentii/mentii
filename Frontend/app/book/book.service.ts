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
import { BookModel } from './book.model';

@Injectable()
export class BookService {
  mentiiConfig = new MentiiConfig();

  constructor (private authHttp: AuthHttp) {
  }

  addBook(bookModel: BookModel):Observable<any> {
    let createClassListUrl = this.mentiiConfig.getRootUrl() + '/book';
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers })
    let body = {
      "title": bookModel.title,
      "description": bookModel.description,
      "chapters": bookModel.chapters
    }
    return this.authHttp.post(createClassListUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }
}
