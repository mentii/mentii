export class MentiiConfig {
  constructor(
  ) {  }

  getRootUrl():string {
    var url:string = 'http://api.mentii.me';
    if (this.isProd() == false) {
      url = 'http://127.0.0.1:5000';
    }
    return url;
  }

  isProd():boolean {
    let _isProd:boolean = false;
    if (window.location.hostname == 'app.mentii.me') {
      _isProd = true;
    }
    return _isProd;
  }
}
