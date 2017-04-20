import { Component, OnInit, Input } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { BookService } from '../book.service';

@Component({
  moduleId: module.id,
  selector: 'bookListItem',
  templateUrl: 'bookListItem.html'
})

export class BookListItemComponent {

  @Input('title')
  public title : string;

  @Input('id')
  public id :string;

  constructor(public bookService: BookService, public toastr: ToastrService){
  }
/*
  ngOnInit() {
  }

  handleSuccess(data) {
    let json = data.json();
    this.books = json.payload.books['Items']
    //this.books = books['payload']
    console.log(this.books);
  }

  handleError(err) {
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }*/

  goToForm() {
    //go to edit book form
  }
}
