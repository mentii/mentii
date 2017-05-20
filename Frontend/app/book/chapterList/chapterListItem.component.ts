import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { SectionListComponent } from '../sectionList/sectionList.component';

@Component({
  moduleId: module.id,
  selector: 'chapterListItem',
  templateUrl: 'chapterListItem.html'
})

export class ChapterListItemComponent {

  @Input('chapter')
  public chapter: FormGroup;

  @Input('index')
  public index: number;

  @Output()
  public onDelete = new EventEmitter<number>();

  delete() {
    this.onDelete.emit(this.index);
  }

  static buildItem() {
    return new FormGroup({
      title: new FormControl('', [Validators.required]),
      sections: SectionListComponent.buildItems()
    });
  }
}
