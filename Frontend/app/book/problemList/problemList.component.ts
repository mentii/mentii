import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
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

  public problemForm: FormGroup;

  public problemFormArray : FormArray;


  constructor(private _formBuilder: FormBuilder){}

  ngOnInit() {
    this.parentSectionForm.addControl('problems', new FormArray([])); //bind to section.problems
    console.log(this.parentSectionForm)
  }

  private toFormGroup(data: ProblemModel) {
    const formGroup = this._formBuilder.group({
        problemString: [ data.problemString ],
    });
    return formGroup;
  }


  addProblem() {
    let problem = new ProblemModel('');
    //console.log('Before Push' + this.problems)
    this.problems.push(problem);
    //console.log('After Push' + this.problems)

  }

  delete(index:number) {
    this.problems.splice(index, 1);
  }

}
