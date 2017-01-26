import { Attribute, Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[clearPlaceholder]'
})

export class ClearPlaceholder {
  plText : string = '';
  constructor(private el: ElementRef) {
    // get original placeholder text
    this.plText = el.nativeElement.getAttribute('placeholder');
  }

  // onFocus set placeholder text to ""
  @HostListener('onFocus') onFocus(){
    this.setPlaceholderText("");
  }

  // onBlur set placeholder text to original placeholder text
  @HostListener('onBlur') onBlur(){
    this.setPlaceholderText(this.plText);
  }

  private setPlaceholderText(text:string) {
    this.el.nativeElement.setAttribute('placeholder', text);
  }
}
