export const ROADS = {
    KOMPOL: 'kompol-11s',
    KOMPOL_10FPS: 'kompol-11s-10fps',
    KOMPOL_2MIN_5FPS: 'kompol-2min-5fps',
}

export const VIDEO_FILES = {
    [ROADS.KOMPOL]: '../static/input.mp4',
    [ROADS.KOMPOL_10FPS]: '../static/input10fps.mp4',
    [ROADS.KOMPOL_2MIN_5FPS]: '../static/new_input5fps.mp4',
}

export const VIDEO_TYPES = {
    [ROADS.KOMPOL]: 'video/mp4',
    [ROADS.KOMPOL_10FPS]: 'video/mp4',
    [ROADS.KOMPOL_2MIN_5FPS]: null,
}