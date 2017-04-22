import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { BookService } from '../book.service';
import { BookModel } from '../book.model';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { ChapterListComponent } from '../chapterList/chapterList.component';

@Component({
  moduleId: module.id,
  selector: 'bookList',
  templateUrl: 'bookList.html'
})

export class BookListComponent implements OnInit{
  public createBookForm: FormGroup;

  books = [];

  // active book model for editing
  selectedBook: BookModel;
  selectedBookId: string;

  isLoading = true;
  editMode = false;

  constructor(private _formBuilder: FormBuilder, public bookService: BookService, public toastr: ToastrService){
  }

  ngOnInit() {
    this.bookService.getAllBooks().subscribe(
      data => this.handleSuccess(data),
      err => this.handleError(err)
    );
  }

  handleSuccess(data) {
    this.books = data.json().payload.books['Items'];
    this.isLoading = false;
  }

  handleError(err) {
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
    this.isLoading = false;
  }

  getFormFromBook(): FormGroup {
    const formGroup = this._formBuilder.group({
      title: [this.selectedBook.title, [Validators.required, Validators.minLength(5)]],
      description: [this.selectedBook.description,[Validators.required]],
      chapters: ChapterListComponent.buildItems()
    });
    return formGroup;
  }

  editBook(book){
    this.selectedBook = book['model'];
    this.selectedBookId = book['bookId'];
    this.createBookForm = this.getFormFromBook();
    this.editMode = true;
  }

  toggleEditMode(){
    this.editMode = !this.editMode;
  }

}
