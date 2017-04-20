import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { BookService } from '../book.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { BookModel } from '../book.model';

@Component({
  moduleId: module.id,
  selector: 'bookEdit',
  templateUrl: 'bookEdit.html'
})

export class BookEditComponent implements OnInit{

  model = new BookModel('', '', []);
  private routeSub: any;
  showTeacherView = false;
  isLoading = true;
  editMode = false;

  constructor(
    public bookService: BookService,
    public toastr: ToastrService,
    private activatedRoute: ActivatedRoute,
    private router: Router){ }

  ngOnInit() {
    //get book details
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.bookService.getBook(params['id'])
      .subscribe(
        data => this.handleSuccess(data.json().payload),
        err => this.handleError(err)
      );
    });

  }

  handleSuccess(data) {
    // populate book model
  }

  handleError(err) {
    let data = err.json();
    for (let error of data['errors']) {
      this.toastr.error(error['message'], error['title']);
    }
  }

}
