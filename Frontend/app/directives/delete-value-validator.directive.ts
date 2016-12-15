import { Directive, forwardRef, Attribute } from '@angular/core';
import { Validator, AbstractControl, NG_VALIDATORS } from '@angular/forms';
@Directive({
  selector: '[deleteValue][formControlName],[deleteValue][formControl],[deleteValue][ngModel]',
  providers: [
    { provide: NG_VALIDATORS, useExisting: forwardRef(() => DeleteValue), multi: true }
  ]
})
export class DeleteValue implements Validator {
  constructor(
    @Attribute('deleteValue') public deleteValue: string) {}

    validate(control: AbstractControl): { [key: string]: any } {
      // control to compare to
      let cleanedControl = control.root.get(this.deleteValue);

      if(cleanedControl && cleanedControl.value) {
        cleanedControl.setValue('');
      }
      return null;
    }
  }
