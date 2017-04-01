import { SectionModel } from './section.model';

export class ChapterModel {
  constructor(
    public title: string,
    public sections: SectionModel[]
  ) {  }
}
