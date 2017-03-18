import { Component, EventEmitter, Input, Output } from '@angular/core';
import { SectionModel } from '../section.model';
import { FormGroup, FormArray, FormControl, Validators } from '@angular/forms';
import { ProblemListComponent } from '../problemList/problemList.component';

@Component({
  moduleId: module.id,
  selector: 'sectionListItem',
  templateUrl: 'sectionListItem.html'
})

export class SectionListItemComponent {
  @Input()
  public section: FormGroup;

  @Input()
  public index: number;

  @Output()
  onDelete = new EventEmitter<number>();

  delete() {
    this.onDelete.emit(this.index);
  }

  static buildItem() {
    return new FormGroup({
      sectionTitle : new FormControl('', Validators.required),
      problems: ProblemListComponent.buildItems()
    })
  }
}
