import { ProblemModel } from './problem.model';

export class SectionModel {
  constructor(
    public title: string,
    public problems: ProblemModel[]
  ) {  }
}
