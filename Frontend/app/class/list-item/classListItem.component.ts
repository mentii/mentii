import { Component, Input } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'class-list-item',
  templateUrl: 'classListItem.html'
})

export class ClassListItemComponent {
  @Input() classObject;
  @Input() classDetailsButton;
  @Input() classJoinButton;
}
