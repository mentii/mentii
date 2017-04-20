// Builtin
import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
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
    let createBookUrl = this.mentiiConfig.getRootUrl() + '/book';
    let body = {
      "title": bookModel.title,
      "description": bookModel.description,
      "chapters": bookModel.chapters
    }
    return this.authHttp.post(createBookUrl, body)
    .map((res:Response) => res)
    .catch((error:any) => Observable.throw(error));
  }

  getBook(bookId: String):Observable<any> {
    let getBookUrl = this.mentiiConfig.getRootUrl() + '/book';
    let body = {
      "id": bookId
    }
    return this.authHttp.get(getBookUrl, body)
      .map((res:Response) => res)
      .catch((error:any) => Observable.throw(error));
  }

  getAllBookTitlesAndIds():Observable<any> {
    let getAllBooksUrl = this.mentiiConfig.getRootUrl() + '/books';
    return this.authHttp.get(getAllBooksUrl)
      .map((res:Response) => res)
      .catch((error:any) => Observable.throw(error));
  }
}
