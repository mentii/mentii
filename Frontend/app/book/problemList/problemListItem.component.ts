import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ProblemModel } from '../problem.model';
import { FormGroup, FormArray, FormBuilder } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'problemListItem',
  templateUrl: 'problemListItem.html'
})

export class ProblemListItemComponent {
  @Input('problems')
  public problems: FormArray;
  @Input('problem')
  public problem: ProblemModel;
  @Input('index')
  public index: number;
  @Output() onDelete = new EventEmitter<number>();

  public problemForm: FormGroup;

  constructor(private  _formBuilder: FormBuilder){}

  ngOnInit() {
    this.problemForm = this.toFormGroup(this.problem);
    this.problems.push(this.problemForm);
  }

  private toFormGroup(data: ProblemModel) {
    const formGroup = this._formBuilder.group({
        problemString: [ data.problemString ],
    });
    return formGroup;
  }

  delete() {
    this.onDelete.emit(this.index);
  }
}
