import { Component, Input } from '@angular/core';
import { ChapterModel } from '../chapter.model';

@Component({
  moduleId: module.id,
  selector: 'chapterList',
  templateUrl: 'list.html'
})

export class ChapterListComponent {
  @Input() chapters;

  addChapter() {
    this.chapters.push(new ChapterModel('','',[]));
  }

  onDelete(index: number) {
    this.chapters.splice(this.chapters.indexOf(index), 1);
    console.log('chapters');
    console.log(this.chapters);
  }
}
