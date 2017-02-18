/*jshint esversion: 6 */
const config = require('/config/config.js');
const mathsteps = require(config.path + 'mathsteps');
const problem = process.argv[2];
const steps = mathsteps.solveEquation(problem);

var responseSteps = [];
steps.forEach( step => {
  if(step.substeps.length > 1) {
    step.substeps.forEach( subStep => {
      responseSteps.push(subStep.newEquation.print());
    }
  );
}
responseSteps.push(step.newEquation.print());
});

var json = JSON.stringify(responseSteps);
console.log(json);
process.exit(0);
