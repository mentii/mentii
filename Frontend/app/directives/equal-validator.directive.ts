import { Directive, forwardRef, Attribute } from '@angular/core';
import { Validator, AbstractControl, NG_VALIDATORS } from '@angular/forms';
@Directive({
  selector: '[validateEqual][formControlName],[validateEqual][formControl],[validateEqual][ngModel]',
  providers: [
    { provide: NG_VALIDATORS, useExisting: forwardRef(() => EqualValidator), multi: true }
  ]
})
export class EqualValidator implements Validator {
  constructor(
    @Attribute('validateEqual') public validateEqual: string) {}

    validate(control: AbstractControl): { [key: string]: any } {
      // control to compare to
      let comparedControl = control.root.get(this.validateEqual);

      if(!control.value || !comparedControl) {
        return null;
      }

      // confirm values are not equal
      if (control.value !== comparedControl.value) {
        return { validateEqual: false }
      }
      return null;
    }
  }
