import { Component, Input, OnInit } from '@angular/core';
import { ProblemModel } from '../problem.model';
import { Validators, FormGroup, FormArray, FormBuilder } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'problemList',
  templateUrl: 'problemList.html'
})

export class ProblemListComponent implements OnInit {
  @Input('parentSectionForm')
  public parentSectionForm: FormGroup;
  @Input('problems')
  public problems: ProblemModel[];

  constructor(private _formBuilder: FormBuilder){}

  ngOnInit() {
    this.parentSectionForm.addControl('problems', new FormArray([]));
  }

  addProblem() {
    this.problems.push(new ProblemModel(''));
  }

  onDelete(index: number) {
    this.problems.splice(index, 1);
  }

}
