import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ChapterModel } from '../chapter.model';

@Component({
  moduleId: module.id,
  selector: 'chapterListItem',
  templateUrl: 'listItem.html'
})

export class ChapterListItemComponent {
  @Input() model;
  @Input() index: number;
  @Output() onDelete = new EventEmitter<number>();

  constructor(){}

  delete() {
    this.onDelete.emit(this.index);
  }
}
