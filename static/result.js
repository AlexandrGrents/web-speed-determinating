export class ResultManager {
    constructor () {
        this.div = $("#result")
        this.video = $("#result-video")
        this.linkWebm = $("#result-link-webm")
        this.linkMp4 = $("#result-link-mp4")
        this.linkJson = $("#result-link-json")

        this.links = {json: this.linkJson, mp4: this.linkMp4, webm: this.linkWebm};
    }

    init (resultData) {
        ['json', 'mp4', 'webm'].forEach(key => {
            if (resultData[key]) {
                const link = this.links[key];

                link.setAttribute('href', resultData[key]);
                link.text(resultData[key]);
                link.show();
            }
        });
    }
}
