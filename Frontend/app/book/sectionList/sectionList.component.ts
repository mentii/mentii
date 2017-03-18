import { Component, Input, OnInit } from '@angular/core';
import { SectionModel } from '../section.model';
import { Validators, FormGroup, FormArray, FormBuilder } from '@angular/forms';
import { SectionListItemComponent } from './sectionListItem.component';

@Component({
  moduleId: module.id,
  selector: 'sectionList',
  templateUrl: 'sectionList.html'
})

export class SectionListComponent implements OnInit {
  @Input()
  public sectionsArray: FormArray;

  constructor(private _formBuilder: FormBuilder){}

  ngOnInit() {
    //this.parentChapterForm.addControl('sectionsArray', new FormArray([]));
  }

  addSection() {
    this.sectionsArray.push(SectionListItemComponent.buildItem());
  }

  static buildItems() {
    return new FormArray([], Validators.required)
  }

}
