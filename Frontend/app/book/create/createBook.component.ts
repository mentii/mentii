import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Validators, FormGroup, FormArray, FormBuilder } from '@angular/forms';
import { BookModel } from '../book.model';
import { BookService } from '../book.service';

@Component({
  moduleId: module.id,
  selector: 'addBook',
  templateUrl: 'createBook.html'
})

export class CreateBookComponent {
  public book: BookModel;
  public createBookForm: FormGroup;

  constructor(private _formBuilder: FormBuilder, public bookService: BookService, public toastr: ToastrService, public router: Router){
  }

  ngOnInit() {
    this.book = new BookModel('', '', []);
    this.createBookForm = this.getFormFromBook(this.book);
  }

  getFormFromBook(data: BookModel): FormGroup {
    const formGroup = this._formBuilder.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      description: [''],
    });
    return formGroup;
  }

  submit(model: FormGroup) {
    console.log(model.value);
    // this.bookService.addBook(this.model).subscribe(
    //   data => this.handleSuccess(),
    //   err => this.handleError(err)
    // );
  }

  handleSuccess() {
    // var message = this.model.title + ' Book Created';
    // this.toastr.success(message);
    // this.router.navigateByUrl('/dashboard');
  }

  handleError(err) {
    // let data = err.json();
    // for (let error of data['errors']) {
    //   this.toastr.error(error['message'], error['title']);
    // }
  }
}
