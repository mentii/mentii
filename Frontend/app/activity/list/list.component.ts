import { Component, Input } from '@angular/core';
import { ActivityModel } from '../activity.model';

@Component({
  moduleId: module.id,
  selector: 'activity-list',
  templateUrl: 'list.html'
})

export class ActivityListComponent {
  @Input() activities;
}
