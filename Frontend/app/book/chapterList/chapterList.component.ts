import { Component, Input, OnInit } from '@angular/core';
import { ChapterModel } from '../chapter.model';
import { Validators, FormGroup, FormArray } from '@angular/forms';
import { ChapterListItemComponent } from './chapterListItem.component';

@Component({
  moduleId: module.id,
  selector: 'chapterList',
  templateUrl: 'chapterList.html'
})

export class ChapterListComponent {

  @Input()
  public chaptersArray: FormArray;

  addChapter() {
    this.chaptersArray.push(ChapterListItemComponent.buildItem());
  }

  static buildItems() {
    return new FormArray([], Validators.required)
  }
}
