import { SectionModel } from './section.model';

export class ChapterModel {
  constructor(
    public title: string,
    public description: string,
    public sections: SectionModel[]
  ) {  }
}
