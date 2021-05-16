
export function getFormData() {
    let body = new FormData();

    let video = $("#video-select").val();
    if (video == "custom") {
        body.set("video", "custom");
        let file = document.getElementById('video-file').files[0];
        if (file) body.set("video-file", file, file.name);
        else {
            alert("Укажите видео-файл");
            return false;
        }
    }
    else body.set("video", video);

    let roadRegion = $("#road-region-select").val();
    if (roadRegion == "custom")
    {
        body.set("roadRegion", "custom");

        let coefsFile = document.getElementById('coefs-file').files[0];
        let maskFile = document.getElementById('mask-file').files[0];

        if (coefsFile && maskFile) {
            body.set("coefsFile", coefsFile, coefsFile.name);
            body.set("maskFile", maskFile, maskFile.name);
        }
        else {
            alert("Укажите файлы с маской и коэффициентами")
            return false;
        }
    }
    else body.set("roadRegion", roadRegion);


    let outputFormat = $('input[name="outputParameters"]:checked').val();
    body.set("outputFormat", outputFormat);

    body.set("bbox", $("#bbox").prop("checked"))
    body.set("class", $("#class").prop("checked"))
    body.set("position", $("#position").prop("checked"))
    body.set("speed", $("#speed").prop("checked"))

    return body;
}

export function showUploadImage(form, showImageElementSelector)  {
    let file = form.files[0];
    if (file) {
        $(showImageElementSelector).show();
        $(showImageElementSelector).attr("src", URL.createObjectURL(file));
    }
    else $(showImageElementSelector).hide();
}

export function setVideoFileUrl(url, type) {
    if (url && type) {
        $("#video-view").show();
        $("#video-view>video").attr("src",url);
        $("#video-view>video").attr("type",type);
        return;
    }
    let file = document.getElementById("video-file").files[0];
    if (file){
        $("#video-view").show();

        let regexp = /mp4$/i;
        if (regexp.test(file.name)) $("#video-view>video").attr("type","video/mp4");
        else $("#video-view>video").attr("type","");

        $("#video-view>video").attr("src",URL.createObjectURL(file));
    }
    else $("#video-view").hide();
}