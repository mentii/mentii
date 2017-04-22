import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { ClassService } from '../class.service';
import { BookService } from '../../book/book.service';
import { ToastrService } from 'ngx-toastr';
import { ClassModel } from '../class.model';
import { ActivityModel } from '../../activity/activity.model';
import { ModalDirective } from 'ng2-bootstrap';
import { NgForm } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'class-detail',
  templateUrl: 'detail.html'
})

export class ClassDetailComponent implements OnInit, OnDestroy {
  model = new ClassModel('', '', '', '', '', [], []);
  private routeSub: any;
  showTeacherView = false;
  isLoading = true;
  @ViewChild('addActivityModal') public autoShownModal:ModalDirective;
  public isModalShown:boolean = false;
  editMode = false;
  newActivity = null;
  books:Array<Object> = [];
  booksDefault = {id: undefined, title: 'Select a Textbook'};
  chapters:Array<Object> = [];
  chaptersDefault = {id: undefined, title: 'Select a Chapter'};
  sections:Array<Object> = [];
  sectionsDefault = {id: undefined, title: 'Select a Section'};

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private classService: ClassService,
    private bookService: BookService,
    private toastr: ToastrService
  ){}

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.model.code = params['id'];
      this.classService.getClass(this.model.code)
      .subscribe(
        data => this.handleSuccess(data.json().payload.class),
        err => this.handleError(err)
      );
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  handleSuccess(data){
    this.model = new ClassModel(
      data.title,
      data.department,
      data.description,
      data.classSection,
      data.code,
      data.activities,
      data.students
    );
    this.showTeacherView = data.isTeacher;
    this.isLoading = false;
  }

  handleError(err){
    this.toastr.error('Unable to access class.');
    this.router.navigateByUrl('/dashboard');
  }

  /* Modal Methods */
  showActivityModal():void {
    this.newActivity = new ActivityModel('', 5, new Date(), new Date(), undefined, undefined, undefined);
    this.resetBooks();
    this.resetChapters();
    this.resetSections();

    this.bookService.getAllBookTitlesAndIds()
      .subscribe(
        data => this.booksRecived(data.json().payload.books),
        err => this.handleGetBooksError(err)
      );
  }

  resetBooks() {
    this.books = [];
    this.books.push(this.booksDefault);
  }

  resetChapters() {
    this.chapters = [];
    this.chapters.push(this.chaptersDefault);
  }

  resetSections() {
    this.sections = [];
    this.sections.push(this.sectionsDefault);
  }

  booksRecived(books) {
    this.books = this.books.concat(books);
    this.isModalShown = true;
  }

  handleGetBooksError(err) {
      this.toastr.error('Unable to load books.');
      this.hideActivityModal();
  }

  hideActivityModal():void {
    this.autoShownModal.hide();
  }

  onHideActivityModal():void {
    this.isModalShown = false;
  }

  bookSelected() {
    this.resetChapters();
    this.resetSections();

    this.bookService.getBook(this.newActivity.bookId)
      .subscribe(
        data => this.bookRecived(data.json().payload),
        err => this.handleGetBookError(err)
      );
  }

  bookRecived(book) {
    console.log(book)
  }

  handleGetBookError(err) {
      this.toastr.error('Unable to load selected book.');
      this.hideActivityModal();
  }

  chapterSelected() {
    this.resetSections();
    //TODO: Load from data
    //this.sections = this.chapters[this.newActivity.chapterTitle]
  }

  sectionSelected() {
    console.log('section selected:' + this.newActivity.sectionTitle);
    //TODO: display sample problems
  }

  /* Edit Methods */
  toggleEditMode(){
    this.editMode = !this.editMode;
  }

  updateModel(form){
    this.model.title = form.value.title;
    this.model.department = form.value.department;
    this.model.section = form.value.section;
    this.model.description = form.value.description;
    this.toggleEditMode();
    this.toastr.success("Class successfully updated.");
  }

  handleUpdateError(err){
    this.toastr.error("Unable to update class details.");
  }

  saveChanges(form: NgForm){
    var newModel = new ClassModel(
      form.value.title,
      form.value.department,
      form.value.description,
      form.value.section,
      this.model.code,
      this.model.activities,
      this.model.students
    );

    this.classService.updateClassDetails(newModel)
      .subscribe(
        data => this.updateModel(form),
        err => this.handleUpdateError(err)
      );
  }
}
