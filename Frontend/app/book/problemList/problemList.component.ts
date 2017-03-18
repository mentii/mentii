import { Component, Input, OnInit } from '@angular/core';
import { ProblemModel } from '../problem.model';
import { Validators, FormGroup, FormArray, FormBuilder } from '@angular/forms';
import { ProblemListItemComponent } from './problemListItem.component';

@Component({
  moduleId: module.id,
  selector: 'problemList',
  templateUrl: 'problemList.html'
})

export class ProblemListComponent implements OnInit {
  @Input()
  public problemsArray: FormArray;

  constructor(private _formBuilder: FormBuilder){}

  ngOnInit() {
    //this.parentSectionForm.addControl('problems', new FormArray([]));
  }

  addProblem() {
    this.problemsArray.push(ProblemListItemComponent.buildItem());
  }

  static buildItems() {
    return new FormArray([], Validators.required)
  }
}
