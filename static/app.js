import {
    getFormData,
    showUploadImage,
    setVideoFileUrl,
} from "./video.js";
import {
    init,
    update,
} from "./init.js";
import {
    ROADS,
    VIDEO_FILES,
    VIDEO_TYPES,
} from "./enums.js";

init();

videoFile.change(setVideoFileUrl);
maskFile.change(function(){showUploadImage(this, "#mask-view")});

videoSelect.change(function() {
    if (this.value === "custom") {
        $("#video-form").show();
        setVideoFileUrl();
    }
    else {
        $("#video-form").hide();
        if (Object.values(ROADS).includes(this.value)) {
            setVideoFileUrl(VIDEO_FILES[this.value], VIDEO_TYPES[this.value])
        }
    }
});

sendVideoForm.submit(function(e){
    e.preventDefault();

    let body = getFormData();
    if (!body) return;

    $.ajax({
        url: globalThis.serverLink,
        type: "POST",
        data: body,
        processData: false,
        contentType: false,
        success: function(data){
            sendVideoForm.hide();

            progressManager.init(data.id);
            $("#send-title").hide();
            progressManager.start();
        }
    });

    return false;
});

update();