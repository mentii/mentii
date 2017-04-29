/*jshint esversion: 6 */

// Imports
const config = require('/config/config.js');
const mathsteps = require(config.path + 'mathsteps');

// Node Arguments
const problem = process.argv[2];
const changeTypesArg = process.argv[3] || "[]"; // empty object is the default value if no object is passed
const showSubStepsFlag = process.argv[4] || "true"; // true is the default value if nothing is passed

// Parsed JSON
const disallowedChangeTypes = JSON.parse(changeTypesArg); // parse argument into workable JSON
const showSubSteps = JSON.parse(showSubStepsFlag); // parse boolean string into boolean type

// Start Solving
var responseSteps = [];
responseSteps.push(problem);
const steps = mathsteps.solveEquation(problem);

// Loops through steps to solve equation
steps.forEach( step => {
  if(step.substeps.length > 1 && showSubSteps) {
    step.substeps.forEach( subStep => {
      if (isChangeAllowed(subStep.changeType)){
        responseSteps.push(subStep.newEquation.print());
      }
    }
  );
  return;
}
if (isChangeAllowed(step.changeType)){
  responseSteps.push(step.newEquation.print());
}
});

// Return Response
var json = JSON.stringify(responseSteps);
console.log(json);
process.exit(0);


/**
* Function to determine if the current step being applied does not exist in the list of step
* types that the user wants to skip.
* @param  {String}  change Current change step being applied to the problem
* @return {Boolean} Returns true if change is not found in list, otherwise false
*/
function isChangeAllowed(change) {
  // disallowedChangeTypes is passed into node as arg 3
  if (disallowedChangeTypes.indexOf(change) > -1) {
    // if active change type is found in array,
    return false;
  }
  // active change type not found in array
  return true;
}
