import { ChapterModel } from './chapter.model';

export class BookModel {
  constructor(
    public title: string,
    public description: string,
    public chapters: ChapterModel[]
  ) {  }
}
