import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { BookService } from '../book.service';

@Component({
  moduleId: module.id,
  selector: 'bookList',
  templateUrl: 'bookList.html'
})

export class BookListComponent implements OnInit{

  books:any;

  constructor(public bookService: BookService, public toastr: ToastrService){
  }

  ngOnInit() {
    this.bookService.getAllBooks().subscribe(
      data => this.handleSuccess(data),
      err => this.handleError(err)
    );
  }

  handleSuccess(data) {
    let json = data.json();
    this.books = json.payload.books['Items'];
  }

  handleError(err) {
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }
}
