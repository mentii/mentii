import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { AppModule } from './app.module';
import { MentiiConfig } from './mentii.config';

if (new MentiiConfig().isOnAws() == true) {
  enableProdMode();
}

const platform = platformBrowserDynamic();
platform.bootstrapModule(AppModule);
