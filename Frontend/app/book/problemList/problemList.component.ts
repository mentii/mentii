import { Component, Input } from '@angular/core';
import { Validators, FormArray } from '@angular/forms';
import { ProblemListItemComponent } from './problemListItem.component';

@Component({
  moduleId: module.id,
  selector: 'problemList',
  templateUrl: 'problemList.html'
})

export class ProblemListComponent{

  @Input('problemsArray')
  public problemsArray: FormArray;

  addProblem() {
    this.problemsArray.push(ProblemListItemComponent.buildItem());
  }

  static buildItems() {
    return new FormArray([])
  }
}
