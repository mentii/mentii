import { Component, Input } from '@angular/core';
import { Validators, FormArray } from '@angular/forms';
import { SectionListItemComponent } from './sectionListItem.component';

@Component({
  moduleId: module.id,
  selector: 'sectionList',
  templateUrl: 'sectionList.html'
})

export class SectionListComponent {

  @Input('sectionsArray')
  public sectionsArray: FormArray;

  addSection() {
    this.sectionsArray.push(SectionListItemComponent.buildItem());
  }

  static buildItems() {
    return new FormArray([]);
  }

}
