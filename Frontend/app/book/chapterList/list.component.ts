import { Component, Input } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'chapter-list',
  templateUrl: 'list.html'
})

export class ChapterListComponent {
  @Input() activities;
}
