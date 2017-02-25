import { Component } from '@angular/core';
import { BookModel } from '../book.model';
import { Router } from '@angular/router';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';
import { BookService } from '../book.service';

@Component({
  moduleId: module.id,
  selector: 'book-create',
  templateUrl: 'create.html'
})

export class CreateBookComponent {
  model = new BookModel('', '', {});

  constructor(public bookService: BookService, public toastr: ToastsManager, public router: Router){
  }

  submit() {
    this.bookService.addBook(this.model).subscribe(
      data => this.handleSuccess(),
      err => this.handleError(err)
    );
  }

  handleSuccess() {
    var message = this.model.title + ' Book Created';
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
