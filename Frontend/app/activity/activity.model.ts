export class ActivityModel {
  constructor(
    public title: string,
    public problemCount: number,
    public targetDate: Date,
    public unlockDate: Date,
    public bookId: string,
    public chapterTitle: string,
    public sectionTitle: string
  ) {  }
}
