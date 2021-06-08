export class ResultManager {
    constructor () {
        this.div = $("#result")
        this.video = $("#result-video")
        this.linkWebm = $("#result-link-webm")
        this.linkMp4 = $("#result-link-mp4")
        this.linkJson = $("#result-link-json")

        this.linksDiv = $("#links");

        this.links = {json: this.linkJson, mp4: this.linkMp4, webm: this.linkWebm};
        Object.values(this.links).forEach(link => link.hide());
        this.video.hide();
    }

    init (resultData) {
        ['json', 'mp4', 'webm'].forEach(key => {
            if (resultData[key]) {
                const link = this.links[key];
                const fileName = resultData[key];
                const src = serverHost + '/file/' + fileName;

                link.attr('href', src);
                link.show();

                if (key === 'webm') {
                    this.video.attr('src', src);
                    this.video.show();
                }
            }
        });

        if (!this.video.is(":visible")) {
            this.linksDiv.removeClass('col-4')
            this.linksDiv.addClass('col-12')
        }
    }
}
