import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ClassModel } from '../class.model';
import { MentiiConfig } from '../../mentii.config';
import { ToastsManager } from 'ng2-toastr/ng2-toastr';

@Component({
  moduleId: module.id,
  selector: 'class-list',
  templateUrl: 'list.html'
})

export class ClassListComponent {
  mentiiConfig = new MentiiConfig();

  classes: ClassModel[] = [
    {
      title: "Algebra 1",
      subtitle: "Introduction to Advanced Math",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque hendrerit mi at massa suscipit, sollicitudin euismod felis lacinia. Phasellus malesuada, enim vitae ultricies ullamcorper, orci eros vestibulum sem, vel tristique justo est ac nisl. Ut sagittis orci feugiat nisi pharetra, ac iaculis odio placerat. Duis ornare congue ultricies. Ut sed commodo neque.",
      code: "d26713cc-f02d-4fd6-80f0-026784d1ab9b"
    },
    {
      title: "Biology 121",
      subtitle: "Flora & Fauna",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque hendrerit mi at massa suscipit, sollicitudin euismod felis lacinia. Phasellus malesuada, enim vitae ultricies ullamcorper, orci eros vestibulum sem, vel tristique justo est ac nisl. Ut sagittis orci feugiat nisi pharetra, ac iaculis odio placerat. Duis ornare congue ultricies. Ut sed commodo neque.",
      code: "d93cd63f-6eda-4644-b603-60f51142749e"
    },
    {
      title: "Business Accounting",
      subtitle: "Taxes and Business Types",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque hendrerit mi at massa suscipit, sollicitudin euismod felis lacinia. Phasellus malesuada, enim vitae ultricies ullamcorper, orci eros vestibulum sem, vel tristique justo est ac nisl. Ut sagittis orci feugiat nisi pharetra, ac iaculis odio placerat. Duis ornare congue ultricies. Ut sed commodo neque.",
      code: "93211750-a753-41cc-b8dc-904d6ed2f931"
    }
  ]

  constructor(public router: Router, public toastr: ToastsManager){
  }

}
