import { Component, Input, OnInit } from '@angular/core';
import { SectionModel } from '../section.model';
import { Validators, FormGroup, FormArray, FormBuilder } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'sectionList',
  templateUrl: 'sectionList.html'
})

export class SectionListComponent implements OnInit {
  @Input('parentChapterForm')
  public parentChapterForm: FormGroup;
  @Input('sections')
  public sections: SectionModel[];

  constructor(private _formBuilder: FormBuilder){}

  ngOnInit() {
    this.parentChapterForm.addControl('sections', new FormArray([]));
  }

  addSection() {
    this.sections.push(new SectionModel('', []));
  }

  onDelete(index: number) {
    this.sections.splice(index, 1);
  }

}
