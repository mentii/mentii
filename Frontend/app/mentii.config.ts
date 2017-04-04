export class MentiiConfig {
  constructor(
  ) {  }

  getRootUrl():string {
    var url:string = 'http://api.mentii.me';
    if (!this.isOnAws()) {
      url = 'http://127.0.0.1:5000';
    }
    if (this.isStaging()){
      url = 'http://stapi.mentii.me';
    }
    return url;
  }

  isStaging():boolean {
    let _isStaging:boolean = false;
    if (window.location.hostname == 'stapp.mentii.me') {
      _isStaging = true;
    }
    return _isStaging;
  }

  isProd():boolean {
    let _isProd:boolean = false;
    if (window.location.hostname == 'app.mentii.me') {
      _isProd = true;
    }
    return _isProd;
  }

  isOnAws():boolean {
    let _enableNgProd:boolean = false;
    if (this.isProd() || this.isStaging()){
      _enableNgProd = true;
    }
    return _enableNgProd;
  }
}
