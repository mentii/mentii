import { Component, OnInit, OnDestroy } from '@angular/core';
import { ProblemService } from '../problem.service';
import { UserService } from '../../user/user.service';
import { ToastrService } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router'


@Component({
  moduleId: module.id,
  selector: 'display-problem',
  templateUrl: 'displayProblem.html'
})

export class DisplayProblemComponent implements OnInit, OnDestroy {

  /*
  Display problem works by showing "good" steps that are less than the current active step count. The
  logic beind the actual showing the step is in displayProblem.html

  If a step object contains a bad step it is immediately shown. When a bad step is shown a "badStepShown" property is added to
  the good step object it belongs to. Badstep paths are walked through in a similar way that the normal steps are walked through, all bad steps within the original step object that are less than the activeBadStepCount are shown.
  */

  private routeSub: any;
  isLoading = true;
  problemTree = null;
  problem = null;
  badStepProblem = null;
  activeStepCount = 0;
  activeBadStepCount = 0;
  badStepShown = false;
  problemIsComplete = false;

  constructor(public problemService: ProblemService, public toastr: ToastrService, public router: Router, private activatedRoute: ActivatedRoute){
  }

  showNextStep(){
    this.activeBadStepCount = 0;
    this.badStepProblem = null;
    let activeStep = this.problemTree[this.activeStepCount+1];
    // If nextstep is clicked, and the next step contains bad steps
    if (activeStep && activeStep.badStep) {
      this.badStepProblem = this.problemTree[this.activeStepCount+1]["badStepPath"];
      this.problemTree[this.activeStepCount+1]['badStepShown'] = true;
      this.activeStepCount++;
    }
    // if the active step is only a good step
    else {
      // if it is a good step and there are no more steps, the problem is complete
      if (this.activeStepCount == this.problemTree.length-1) {
        this.problemIsComplete = true;
      }
      // if more steps exist, increment the counter so the next good step is shown on the page
      this.activeStepCount++;
    }
  }

  showNextBadStep(){
    if (this.activeBadStepCount == this.badStepProblem.length-1) {
      this.toastr.error("This doesn't seem quite right", "Uh Oh");
    } else {
      this.activeBadStepCount++;
    }
  }

  incorrectBadStep() {
    this.toastr.success("This was an incorrect step, that you corrected", "Good Job");
    this.problemTree[this.activeStepCount]['badStepShown'] = false;
  }

  incorrectGoodStep() {
    this.toastr.error("This is actually a correct step to take.", "Sorry");
  }

  returnToClassPage() {
    this.activatedRoute.params.subscribe(params => {
      let classCode = params['classCode'];
      this.router.navigateByUrl('/class/' + classCode);
    });
  }

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      // grab codes out of the URL
      let classCode = params['classCode'];
      let problemCode = params['problemCode'];
      this.problemService.getProblemSteps(classCode,problemCode)
      .subscribe(
        data => this.handleInitSuccess(data.json()),
        err => this.handleInitError(err)
      );
    });
  }

  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }

  handleInitSuccess(data) {
    //save the problem
    this.problemTree = data.payload.problemTree;
    //save the equation being solved as different variable
    this.problem = data.payload.problemTree[0].correctStep;
    this.isLoading = false;
  }

  handleInitError(err) {
    this.isLoading = false;
    if (!err.isAuthenticationError) {
      this.toastr.error('The problem steps failed to load.');
    }
  }
}
