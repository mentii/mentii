import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule }    from '@angular/http';
import { FormsModule }   from '@angular/forms';
import { AppComponent } from './app.component';
import { RegistrationComponent }   from './registration/registration.component';
import { RootComponent }   from './root/root.component';
import { routing } from './app.routes';

@NgModule({
  imports:      [ BrowserModule, FormsModule, HttpModule, routing],
	declarations: [ AppComponent, RegistrationComponent, RootComponent ],
	bootstrap:    [ AppComponent ]
})
export class AppModule { }
