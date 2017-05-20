import { Component, Input } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'activity-list',
  templateUrl: 'list.html'
})

export class ActivityListComponent {
  @Input() activities;
  @Input() classCode;
  @Input() isStudentInClass;
  @Input() isTeacher;

  isAfterStartDate(activity) {
    if (new Date(activity.startDate) <= new Date())
      return true;
    return false;
  }
}
