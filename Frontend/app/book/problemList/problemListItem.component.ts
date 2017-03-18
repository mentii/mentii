import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ProblemModel } from '../problem.model';
import { FormGroup, Validators, FormControl } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'problemListItem',
  templateUrl: 'problemListItem.html'
})

export class ProblemListItemComponent {
  @Input()
  public problem: FormGroup;

  @Input()
  public index: number;

  @Output()
  onDelete = new EventEmitter<number>();

  delete() {
    this.onDelete.emit(this.index);
  }

  static buildItem() {
    return new FormGroup({
      problemString : new FormControl('', Validators.required)
    })
  }
}
