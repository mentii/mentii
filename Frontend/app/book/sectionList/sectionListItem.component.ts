import { Component, EventEmitter, Input, Output } from '@angular/core';
import { SectionModel } from '../section.model';
import { FormGroup, FormArray, FormBuilder } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'sectionListItem',
  templateUrl: 'sectionListItem.html'
})

export class SectionListItemComponent {
  @Input('sections')
  public sections: FormArray;
  @Input('section')
  public section: SectionModel;
  @Input('index')
  public index: number;
  @Output() onDelete = new EventEmitter<number>();

  public sectionForm: FormGroup;

  constructor(private  _formBuilder: FormBuilder){}

  ngOnInit() {
    this.sectionForm = this.toFormGroup(this.section);
    this.sections.push(this.sectionForm);
  }

  private toFormGroup(data: SectionModel) {
    const formGroup = this._formBuilder.group({
        title: [ data.title ],
    });
    return formGroup;
  }

  delete() {
    this.onDelete.emit(this.index);
  }
}
