import { Component, Input } from '@angular/core';
import { Validators, FormArray } from '@angular/forms';
import { ChapterListItemComponent } from './chapterListItem.component';

@Component({
  moduleId: module.id,
  selector: 'chapterList',
  templateUrl: 'chapterList.html'
})

export class ChapterListComponent {

  @Input('chaptersArray')
  public chaptersArray: FormArray;

  addChapter() {
    this.chaptersArray.push(ChapterListItemComponent.buildItem());
  }

  static buildItems() {
    return new FormArray([]);
  }
}
