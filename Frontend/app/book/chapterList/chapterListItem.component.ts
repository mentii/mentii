import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ChapterModel } from '../chapter.model';
import { FormGroup, FormArray, FormBuilder } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'chapterListItem',
  templateUrl: 'chapterListItem.html'
})

export class ChapterListItemComponent {
  @Input('chapters')
  public chapters: FormArray;
  @Input('chapter')
  public chapter: ChapterModel;
  @Input('index')
  public index: number;
  @Output() onDelete = new EventEmitter<number>();

  public chapterForm: FormGroup;

  constructor(private  _formBuilder: FormBuilder){}

  ngOnInit() {
    this.chapterForm = this.toFormGroup(this.chapter);
    this.chapters.push(this.chapterForm);
  }

  private toFormGroup(data: ChapterModel) {
    const formGroup = this._formBuilder.group({
        title: [ data.title ],
    });
    return formGroup;
  }

  delete() {
    this.onDelete.emit(this.index);
  }
}
