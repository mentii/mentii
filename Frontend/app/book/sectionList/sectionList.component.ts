import { Component, Input, OnInit } from '@angular/core';
import { ChapterModel } from '../chapter.model';
import { Validators, FormGroup, FormArray, FormBuilder } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'chapterList',
  templateUrl: 'chapterList.html'
})

export class ChapterListComponent implements OnInit {
  @Input('parentBookForm')
  public parentBookForm: FormGroup;
  @Input('chapters')
  public chapters: ChapterModel[];

  constructor(private _formBuilder: FormBuilder){}

  ngOnInit() {
    this.parentBookForm.addControl('chapters', new FormArray([]));
  }

  addChapter() {
    this.chapters.push(new ChapterModel('', []));
  }

  onDelete(index: number) {
    this.chapters.splice(index, 1);
  }

}
