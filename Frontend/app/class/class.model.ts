import { ActivityModel } from '../activity/activity.model';

export class ClassModel {
  constructor(
    public title: string,
    public department: string,
    public description: string,
    public section: string,
    public code: string,
    public activities: ActivityModel[],
    public students: string[]
  ) {  }
}
