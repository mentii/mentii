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
  chapterData = null;
  sectionData = null;
  sampleProblems = [];

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private classService: ClassService,
    private bookService: BookService,
    private toastr: ToastrService
  ){}

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(qParams => {
      if(qParams['edit'] == 'true') {
        this.editMode = true;
      }
    });

    this.routeSub = this.activatedRoute.params.subscribe(params => {
      this.model.code = params['id'];
      this.classService.getClass(this.model.code)
      .subscribe(
        data => this.handleSuccess(data.json().payload.class),
        err => this.handleError()
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

  handleError(){
    this.toastr.error('Unable to access class.');
    this.router.navigateByUrl('/dashboard');
  }

  /* Modal Methods */
  showActivityModal():void {
    this.newActivity = new ActivityModel('', 5, undefined, undefined, undefined, undefined, undefined);
    this.resetBooks();

    this.bookService.getAllBookTitlesAndIds()
      .subscribe(
        data => this.booksRecived(data.json().payload.books),
        err => this.handleGetBooksError()
      );
  }

  resetBooks() {
    this.books = [];
    this.books.push(this.booksDefault);
    this.resetChapters();
  }

  resetChapters() {
    this.chapterData = null;
    this.chapters = [];
    this.chapters.push(this.chaptersDefault);
    this.resetSections();
  }

  resetSections() {
    this.sectionData = null;
    this.sections = [];
    this.sections.push(this.sectionsDefault);
  }

  booksRecived(books) {
    this.books = this.books.concat(books);
    this.isModalShown = true;
  }

  handleGetBooksError() {
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
    if(this.newActivity.bookId == null)
      return;

    this.resetChapters();
    this.chapterData = null;

    this.bookService.getBook(this.newActivity.bookId)
      .subscribe(
        data => this.bookRecived(data.json().payload),
        err => this.handleGetBookError()
      );
  }

  bookRecived(book) {
    this.chapterData = book.chapters;
    for (var i = 0; i < this.chapterData.length; i++) {
      this.chapters.push({
        'id': i,
        'title': this.chapterData[i].title
      })
    }
  }

  handleGetBookError() {
      this.toastr.error('Unable to load selected book.');
      this.hideActivityModal();
  }

  chapterSelected(chapterIndex) {
    this.resetSections();
    if(chapterIndex == "undefined")
      return;
    this.newActivity.chapterTitle = this.chapterData[chapterIndex].title;
    this.sectionData = this.chapterData[chapterIndex].sections;
    for (var sectionIndex = 0; sectionIndex < this.sectionData.length; sectionIndex++) {
      this.sections.push({
        'id': sectionIndex,
        'title': this.sectionData[sectionIndex].title
      })
    }
  }

  sectionSelected(sectionIndex) {
    if(sectionIndex == "undefined")
      return;
    this.newActivity.sectionTitle = this.sectionData[sectionIndex].title;
    this.bookService.getSampleProblems(
        this.newActivity.bookId,
        this.newActivity.chapterTitle,
        this.newActivity.sectionTitle)
      .subscribe(
        data => this.problemsRecived(data.json().payload.problems),
        err => this.handleGetProblemsError()
      );
  }

  problemsRecived(problems) {
    this.sampleProblems = problems;
  }

  handleGetProblemsError() {
    this.toastr.error('Unable to load sample problems.');
  }

  addActivity() {
    this.classService.addActivity(this.model.code, this.newActivity)
      .subscribe(
        data => this.activityAdded(),
        err => this.handleAddActivityError()
      );
  }

  activityAdded() {
    this.toastr.success('New activity added.');
    this.ngOnInit();
    this.onHideActivityModal();
  }

  handleAddActivityError() {
    this.toastr.error('Unable to add activity.');
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

  handleUpdateError(){
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
        err => this.handleUpdateError()
      );
  }
}
