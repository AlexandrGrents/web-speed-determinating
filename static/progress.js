import {ResultManager} from "./result.js";

export class ProgressManager {
    constructor () {
        this._progressHtml = $("#detectionProgressbar");
        this._progressText = $("#progress-text");

        this._resultManager = new ResultManager();
    }

    init (processId) {
        this._processId = processId
    }

    start () {
        this.updateHtml({
            currentFrame: 0,
            frameCount: 1,
        });
        $("#detectionProccess").show();
        $.ajax({
            url: globalThis.progressLink + this._processId,
            type: "GET",
            processData: false,
            contentType: false,
            success: this.update.bind(this)
        });
    }

    update (data) {
        if (data.status === 'end') {
            return this.stop(data);
        }

        this.updateHtml(data);

        setTimeout(() => {
            $.ajax({
                url: globalThis.progressLink + this._processId,
                type: "GET",
                processData: false,
                contentType: false,
                success: this.update.bind(this)
            });
        }, 2000);
    }

    /**
     *
     * @param {Object} data
     * @param data.webm
     */
    stop (data) {
        $("#result").show();
        this._progressHtml.hide();
        this._progressText.hide();
        console.log('stop', data)
        $("#detectionProccess").hide();
        document.cookie = `process_id=0`

        this._resultManager.init(data);
    }

    /**
     * @param {Object} data
     * @param data.currentFrame
     * @param data.frameCount
     */
    updateHtml (data) {
        if (!data.currentFrame) data.currentFrame = 0;
        if (!data.frameCount) data.frameCount = 1;

        const p = Math.floor(100 * data.currentFrame / data.frameCount);
        this._progressHtml.css("width", p + '%');
        this._progressHtml.text(p + '%');

        this._progressText.text(`${data.currentFrame} / ${data.frameCount}`);
    }
}