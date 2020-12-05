export default class Application{
	constructor(){
		this.conntect = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/sio');
	}
}