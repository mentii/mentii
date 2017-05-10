export class ActivityModel {
  constructor(
    public title: string,
    public description: string,
    public problemCount: number,
    public startDate: Date,
    public dueDate: Date,
    public bookId: string,
    public chapterTitle: string,
    public sectionTitle: string
  ) {  }
}
