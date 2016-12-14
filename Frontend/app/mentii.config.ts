export class MentiiConfig {
  constructor(
  ) {  }

  getRootUrl() {
    var environment:string;
    var url = '';
    environment = window.location.hostname;
    switch (environment) {
      case'localhost': {
        url = 'http://127.0.0.1:5000';
      };
      break;
      case 'app.mentii.me': {
        url = 'http://api.mentii.me';
        break;
      };
      default: {
        url = 'http://api.mentii.me';
      };
    }
    return url;
  }
}
