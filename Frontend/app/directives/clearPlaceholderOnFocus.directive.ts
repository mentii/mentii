import { Attribute, Directive, ElementRef, HostListener, Input, Renderer } from '@angular/core';

@Directive({
  selector: '[clearPlaceholder]',
  host:{
    'onfocus' : 'onFocus()',
    'onblur' : 'onBlur()'
  }
})

export class ClearPlaceholder {
  plText : string = '';
  element;
  constructor(public el: ElementRef, public renderer: Renderer) {
    // get element
    this.element = this.renderer.selectRootElement(el.nativeElement);

    // get original placeholder text
    this.plText = this.element.getAttribute('placeholder');
    console.log(this.plText);
  }

  // onFocus set placeholder text to ""
  @HostListener('onfocus') onFocus(){
    console.log('onFocus');
    this.setPlaceholderText("");
  }

  // onBlur set placeholder text to original placeholder text
  @HostListener('onblur') onBlur(){
    console.log('onBlur');
    this.setPlaceholderText(this.plText);
  }

  private setPlaceholderText(text:string) {
    this.renderer.setElementAttribute(this.element,'placeholder', text);
  }
}
