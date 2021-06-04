

export function init () {
    globalThis.serverHost = location.href;
    globalThis.serverLink = globalThis.serverHost + "/detect"
    globalThis.progressLink = globalThis.serverHost + "/result/"

    globalThis.videoFile = $("#video-file");
    globalThis.maskFile = $("#mask-file");
    globalThis.videoSelect = $("#video-select");
    globalThis.sendVideoForm = $("#sendVideoForm")
    globalThis.resultSection = $("#result");
}

export function update () {
    videoFile.change();
    maskFile.change();
    videoSelect.change();

    $("#detectionProccess").hide();
    resultSection.hide();
}
