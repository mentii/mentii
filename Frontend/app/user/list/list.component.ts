import { Component, Input } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'user-list',
  templateUrl: 'list.html'
})

export class UserListComponent {
  @Input() users;
}
