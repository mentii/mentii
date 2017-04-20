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

  constructor(public bookService: BookService, public toastr: ToastrService){ }

  goToForm() {
    //go to edit book form
  }
}
