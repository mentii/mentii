import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { BookModel } from '../book.model';

@Component({
  moduleId: module.id,
  selector: 'bookListItem',
  templateUrl: 'bookListItem.html'
})

export class BookListItemComponent implements OnInit {

  @Input('book')
  public book;

  @Output() selection = new EventEmitter();

  title: string;
  model = new BookModel('','',[]);

  constructor(){ }

  ngOnInit() {
    this.title = this.book.title;
    this.model.title = this.book.title;
    this.model.description = this.book.description;
    this.model.chapters = this.book.chapters;
  }

  selectBook() {
    this.selection.emit({'model':this.model, 'bookId': this.book.bookId });
  }
}
