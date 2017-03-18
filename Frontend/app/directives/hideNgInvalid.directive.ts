import { Attribute, Directive, ElementRef, Renderer, AfterViewInit } from '@angular/core';

@Directive({
  selector: '[hideNgInvalid]',
})

export class HideNgInvalid implements AfterViewInit {
  plText : string = '';
  element;

  constructor(public el: ElementRef, public renderer: Renderer) {
    // get element
    this.element = this.renderer.selectRootElement(el.nativeElement);

    // remove ng-invalid attribute from class when user is typing
    this.renderer.listen(this.element, 'input', (event) => {
      let isInvalid = this.element.getAttribute('class').search('ng-invalid');

      if(isInvalid != -1) {
        let newClass = this.element.getAttribute('class').replace('ng-invalid', '');
        this.renderer.setElementAttribute(this.element, 'class', newClass);
      }
    })

    // remove ng-invalid attribute from class after user clicks Add New __
    this.renderer.listen(this.element, 'click', (event) => {
      let isInvalid = this.element.getAttribute('class').search('ng-invalid');

      if(isInvalid != -1) {
        let newClass = this.element.getAttribute('class').replace('ng-invalid', '');
        this.renderer.setElementAttribute(this.element, 'class', newClass);
      }
    })
  }

  ngAfterViewInit() {
    let isInvalid = this.element.getAttribute('class').search('ng-invalid');

    if(isInvalid != -1) {
      let newClass = this.element.getAttribute('class').replace('ng-invalid', '');
      this.renderer.setElementAttribute(this.element, 'class', newClass);
    }
  }
}
