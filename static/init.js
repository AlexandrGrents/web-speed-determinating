

export function init () {
    globalThis.serverHost = "http://127.0.0.1:5000"
    globalThis.serverLink = globalThis.serverHost + "/detect"
    globalThis.progressLink = globalThis.serverHost + "/result/"

    globalThis.videoFile = $("#video-file");
    globalThis.maskFile = $("#mask-file");
    globalThis.videoSelect = $("#video-select");
    globalThis.roadRegionSelect = $("#road-region-select" );
    globalThis.sendVideoForm = $("#sendVideoForm")
    globalThis.resultSection = $("#result");
}

export function update () {
    videoFile.change();
    maskFile.change();
    videoSelect.change();
    roadRegionSelect.change();

    resultSection.hide();
}