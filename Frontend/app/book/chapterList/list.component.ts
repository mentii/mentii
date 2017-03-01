import { Component, Input } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'chapterList',
  templateUrl: 'list.html'
})

export class ChapterListComponent {
  @Input() chapters;

  addChapter() {
    console.log('Alright')
  }
}
