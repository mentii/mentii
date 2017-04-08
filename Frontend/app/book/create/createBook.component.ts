import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { BookService } from '../book.service';
import { ChapterListComponent } from '../chapterList/chapterList.component';

@Component({
  moduleId: module.id,
  selector: 'addBook',
  templateUrl: 'createBook.html'
})

export class CreateBookComponent {
  public createBookForm: FormGroup;

  constructor(private _formBuilder: FormBuilder, public bookService: BookService, public toastr: ToastrService, public router: Router){
  }

  ngOnInit() {
    this.createBookForm = this.getFormFromBook();
  }

  getFormFromBook(): FormGroup {
    const formGroup = this._formBuilder.group({
      title: ['', [Validators.required, Validators.minLength(5)]],
      description: ['',[Validators.required]],
      chapters: ChapterListComponent.buildItems()
    });
    return formGroup;
  }

  submit(model: FormGroup) {
    this.bookService.addBook(model.value).subscribe(
      data => this.handleSuccess(model.value),
      err => this.handleError(err)
    );
  }

  handleSuccess(model) {
    var message = model.title + ' Book Created';
    this.toastr.success(message);
    this.router.navigateByUrl('/dashboard');
  }

  handleError(err) {
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }
}
