import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ProblemService } from '../problem.service';
import { UserService } from '../../user/user.service';
import { ToastrService } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';


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
  problemIndex = 0;
  classCode = '';
  problemCode = '';

  stepIsBeingCorrected = false;
  correctionModel = {
    correction: '',
    stepToCorrect: ''
  }

  // default red color is not shown
  showBadStepColor = false;
  panelClass = 'panel panel-default';

  //default all bad steps in tree are shown
  selectedStepLimit = -1;
  stepLimit = 0;

  constructor(public problemService: ProblemService, public toastr: ToastrService, public router: Router, private activatedRoute: ActivatedRoute){
  }

  applyCorrection() {
    let trimmedCorrection = this.correctionModel.correction.replace(/\s+/g, ''); // Removed all whitespace
    let trimmedActual = this.problemTree[this.activeStepCount].correctStep.replace(/\s+/g, ''); // Removed all whitespace
    if (trimmedCorrection == trimmedActual) {
      this.toastr.success("Your correction got Mentii back on the right path", "Good Job");
      this.problemTree[this.activeStepCount]['badStepShown'] = false; // Close the bad step subtree
      this.stepIsBeingCorrected = false;
      this.showNextStep(); // Progress to the next step, after the correction
    } else {
      this.toastr.error("Your correction won't help Mentii get back on the right path", "Not Quite...");
    }
  }

  cancelCorrection() {
    this.stepIsBeingCorrected = false;
    this.correctionModel.correction = ''; //clear the correction from the text box
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
      this.setStepLimit();
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
    // TODO print for testing purposes, will remove in final product
    console.log('Active Step Count: ' + this.activeBadStepCount);
    console.log('Step Limit: ' + this.stepLimit);
    if (this.activeBadStepCount >= this.stepLimit) {
      this.sendFailUpdate();
      this.toastr.error("This doesn't seem quite right", "Uh Oh");
    } else {
      this.activeBadStepCount++;
    }
  }

  incorrectBadStep(badStepIndex: number, problemStep: string) {
    if (badStepIndex == 0) {
      this.correctionModel.correction = this.badStepProblem[0]; //set the model to the current bad step
      this.stepIsBeingCorrected = true;
    } else {
      this.toastr.warning("This is part of an incorrect step, but the problem is in a different step", "Almost...");
    }
  }

  incorrectGoodStep() {
    this.toastr.error("This is actually a correct step to take.", "Sorry");
  }

  returnToClassPage() {
    this.sendSuccessUpdate();
    this.activatedRoute.params.subscribe(params => {
      let classCode = params['classCode'];
      this.router.navigateByUrl('/class/' + classCode);
    });
  }

  sendSuccessUpdate() {
    this.problemService.postProblemSuccess(this.classCode, this.problemCode, this.problemIndex, "True")
      .subscribe();
  }
  
  sendFailUpdate() {
    this.problemService.postProblemSuccess(this.classCode, this.problemCode, this.problemIndex, "")
      .subscribe();
  }

  ngOnInit() {
    this.routeSub = this.activatedRoute.params.subscribe(params => {
      // grab codes out of the URL
      this.classCode = params['classCode'];
      this.problemCode = params['problemCode'];
      this.problemService.getProblemSteps(this.classCode,this.problemCode)
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
    this.problemIndex = data.payload.problemIndex;
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

  selectStepLimit(limit){
    this.selectedStepLimit = limit;
  }

  setStepLimit(){
    let limit = this.selectedStepLimit-1;
    if(limit < 0){
      this.stepLimit = this.badStepProblem.length-1;
    }
    else {
      this.stepLimit = limit;
    }
  }

  toggleBadStepColor(){
    this.showBadStepColor = !this.showBadStepColor;
    if(this.showBadStepColor){
      this.panelClass = 'panel panel-danger';
    } else{
      this.panelClass = 'panel panel-default';
    }
  }
}
