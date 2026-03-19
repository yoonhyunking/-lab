{\rtf1\ansi\ansicpg949\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import numpy as np\
from PIL import Image, ImageEnhance, ImageFilter, ImageOps\
import io\
import random\
\
st.set_page_config(\
    page_title="FilmLab - \uc0\u54596 \u47492  \u52852 \u47700 \u46972  \u48372 \u51221 ",\
    page_icon="\uc0\u55357 \u56567 ",\
    layout="wide",\
)\
\
st.markdown("""\
<style>\
    .main-title \{\
        font-size: 2.4rem;\
        font-weight: 800;\
        letter-spacing: -0.5px;\
        margin-bottom: 0.2rem;\
    \}\
    .subtitle \{\
        color: #888;\
        font-size: 1rem;\
        margin-bottom: 2rem;\
    \}\
    .filter-card \{\
        border: 2px solid transparent;\
        border-radius: 12px;\
        padding: 4px;\
        cursor: pointer;\
        transition: border-color 0.2s;\
    \}\
    .filter-card:hover \{\
        border-color: #f4a261;\
    \}\
    .stButton > button \{\
        border-radius: 10px;\
        font-weight: 600;\
        transition: all 0.2s;\
    \}\
    div[data-testid="stImage"] img \{\
        border-radius: 12px;\
    \}\
    .film-badge \{\
        display: inline-block;\
        background: #1a1a2e;\
        color: #f4a261;\
        border-radius: 20px;\
        padding: 4px 12px;\
        font-size: 0.75rem;\
        font-weight: 700;\
        letter-spacing: 1px;\
        text-transform: uppercase;\
        margin-bottom: 8px;\
    \}\
    .section-label \{\
        font-size: 0.75rem;\
        font-weight: 700;\
        letter-spacing: 1.5px;\
        text-transform: uppercase;\
        color: #888;\
        margin-bottom: 0.5rem;\
    \}\
</style>\
""", unsafe_allow_html=True)\
\
\
FILM_PRESETS = \{\
    "\uc0\u50896 \u48376 ": \{\
        "description": "\uc0\u48372 \u51221  \u50630 \u51060  \u50896 \u48376  \u44536 \u45824 \u47196 ",\
        "brightness": 1.0,\
        "contrast": 1.0,\
        "saturation": 1.0,\
        "warmth": 0,\
        "shadows_lift": 0,\
        "highlight_cut": 0,\
        "grain": 0,\
        "vignette": 0,\
        "fade": 0,\
        "green_cast": 0,\
        "red_boost": 0,\
        "blue_cut": 0,\
        "cyan_boost": 0,\
        "bw": False,\
        "icon": "\uc0\u55357 \u56764 \u65039 ",\
    \},\
    "Kodak Portra 400": \{\
        "description": "\uc0\u46384 \u46907 \u54616 \u44256  \u51088 \u50672 \u49828 \u47084 \u50868  \u49828 \u53416 \u53668 , \u51064 \u47932  \u49324 \u51652 \u50640  \u52572 \u51201 ",\
        "brightness": 1.08,\
        "contrast": 0.92,\
        "saturation": 0.88,\
        "warmth": 18,\
        "shadows_lift": 12,\
        "highlight_cut": 8,\
        "grain": 18,\
        "vignette": 0.18,\
        "fade": 10,\
        "green_cast": 4,\
        "red_boost": 10,\
        "blue_cut": 8,\
        "cyan_boost": 0,\
        "bw": False,\
        "icon": "\uc0\u55356 \u57093 ",\
    \},\
    "Kodak Gold 200": \{\
        "description": "\uc0\u54889 \u44552 \u48731  \u50668 \u47492  \u45712 \u45196 , \u48712 \u54000 \u51648  \u44048 \u49457 ",\
        "brightness": 1.05,\
        "contrast": 1.05,\
        "saturation": 1.15,\
        "warmth": 25,\
        "shadows_lift": 8,\
        "highlight_cut": 5,\
        "grain": 22,\
        "vignette": 0.22,\
        "fade": 8,\
        "green_cast": 6,\
        "red_boost": 18,\
        "blue_cut": 14,\
        "cyan_boost": 0,\
        "bw": False,\
        "icon": "\uc0\u9728 \u65039 ",\
    \},\
    "Fuji Velvia 50": \{\
        "description": "\uc0\u49440 \u47749 \u54616 \u44256  \u52292 \u46020  \u45458 \u51008  \u51088 \u50672  \u54413 \u44221 \u50857 ",\
        "brightness": 1.0,\
        "contrast": 1.18,\
        "saturation": 1.45,\
        "warmth": -6,\
        "shadows_lift": 0,\
        "highlight_cut": 10,\
        "grain": 8,\
        "vignette": 0.14,\
        "fade": 0,\
        "green_cast": 12,\
        "red_boost": 0,\
        "blue_cut": -5,\
        "cyan_boost": 8,\
        "bw": False,\
        "icon": "\uc0\u55356 \u57151 ",\
    \},\
    "Fuji Pro 400H": \{\
        "description": "\uc0\u54028 \u49828 \u53588  \u53668 , \u48512 \u46300 \u47101 \u44256  \u52397 \u47049 \u54620  \u45712 \u45196 ",\
        "brightness": 1.12,\
        "contrast": 0.88,\
        "saturation": 0.80,\
        "warmth": -10,\
        "shadows_lift": 18,\
        "highlight_cut": 12,\
        "grain": 14,\
        "vignette": 0.12,\
        "fade": 16,\
        "green_cast": 8,\
        "red_boost": -5,\
        "blue_cut": -10,\
        "cyan_boost": 12,\
        "bw": False,\
        "icon": "\uc0\u55356 \u57144 ",\
    \},\
    "Ilford HP5 (\uc0\u55121 \u48177 )": \{\
        "description": "\uc0\u53364 \u47000 \u49885  \u55121 \u48177 , \u44053 \u54620  \u45824 \u48708 \u50752  \u44618 \u51060 ",\
        "brightness": 1.0,\
        "contrast": 1.15,\
        "saturation": 0,\
        "warmth": 0,\
        "shadows_lift": 5,\
        "highlight_cut": 5,\
        "grain": 28,\
        "vignette": 0.28,\
        "fade": 5,\
        "green_cast": 0,\
        "red_boost": 0,\
        "blue_cut": 0,\
        "cyan_boost": 0,\
        "bw": True,\
        "icon": "\uc0\u11035 ",\
    \},\
    "Kodak T-MAX (\uc0\u55121 \u48177 )": \{\
        "description": "\uc0\u49464 \u48128 \u54620  \u44536 \u47112 \u51064 , \u48512 \u46300 \u47084 \u50868  \u55121 \u48177 ",\
        "brightness": 1.04,\
        "contrast": 1.08,\
        "saturation": 0,\
        "warmth": 5,\
        "shadows_lift": 10,\
        "highlight_cut": 8,\
        "grain": 14,\
        "vignette": 0.20,\
        "fade": 8,\
        "green_cast": 0,\
        "red_boost": 0,\
        "blue_cut": 0,\
        "cyan_boost": 0,\
        "bw": True,\
        "icon": "\uc0\u55356 \u57105 ",\
    \},\
    "Agfa Vista (\uc0\u54168 \u51060 \u46300 )": \{\
        "description": "\uc0\u48712 \u54000 \u51648  \u49353  \u48148 \u47016 , \u47112 \u53944 \u47196  \u44048 \u49457 ",\
        "brightness": 1.06,\
        "contrast": 0.85,\
        "saturation": 0.75,\
        "warmth": 12,\
        "shadows_lift": 22,\
        "highlight_cut": 8,\
        "grain": 24,\
        "vignette": 0.30,\
        "fade": 25,\
        "green_cast": 10,\
        "red_boost": 8,\
        "blue_cut": 5,\
        "cyan_boost": 0,\
        "bw": False,\
        "icon": "\uc0\u55357 \u56572 ",\
    \},\
    "Lomo LC-A": \{\
        "description": "\uc0\u44053 \u54620  \u48708 \u45348 \u54021 \u44284  \u52292 \u46020 , \u47196 \u47784 \u44536 \u47000 \u54588  \u49828 \u53440 \u51068 ",\
        "brightness": 0.95,\
        "contrast": 1.25,\
        "saturation": 1.35,\
        "warmth": 8,\
        "shadows_lift": -5,\
        "highlight_cut": 15,\
        "grain": 30,\
        "vignette": 0.55,\
        "fade": 0,\
        "green_cast": 0,\
        "red_boost": 12,\
        "blue_cut": 5,\
        "cyan_boost": 5,\
        "bw": False,\
        "icon": "\uc0\u55357 \u56622 ",\
    \},\
    "Cross Process": \{\
        "description": "\uc0\u49836 \u46972 \u51060 \u46300  \u54596 \u47492 \u51012  C-41 \u54788 \u49345 , \u44053 \u47148 \u54620  \u49353 \u49345  \u50780 \u44257 ",\
        "brightness": 1.05,\
        "contrast": 1.30,\
        "saturation": 1.40,\
        "warmth": -15,\
        "shadows_lift": -8,\
        "highlight_cut": 20,\
        "grain": 20,\
        "vignette": 0.25,\
        "fade": 0,\
        "green_cast": 20,\
        "red_boost": 15,\
        "blue_cut": -15,\
        "cyan_boost": 15,\
        "bw": False,\
        "icon": "\uc0\u55356 \u57256 ",\
    \},\
\}\
\
\
def add_grain(img_array, intensity):\
    if intensity == 0:\
        return img_array\
    noise = np.random.normal(0, intensity, img_array.shape).astype(np.int16)\
    result = img_array.astype(np.int16) + noise\
    return np.clip(result, 0, 255).astype(np.uint8)\
\
\
def add_vignette(img_array, strength):\
    if strength == 0:\
        return img_array\
    h, w = img_array.shape[:2]\
    y, x = np.ogrid[:h, :w]\
    cx, cy = w / 2, h / 2\
    dist = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2)\
    dist = dist / dist.max()\
    vignette = 1 - (dist ** 1.5) * strength\
    vignette = np.clip(vignette, 0, 1)\
    if len(img_array.shape) == 3:\
        vignette = vignette[:, :, np.newaxis]\
    result = img_array.astype(np.float32) * vignette\
    return np.clip(result, 0, 255).astype(np.uint8)\
\
\
def adjust_warmth(img_array, amount):\
    if amount == 0:\
        return img_array\
    result = img_array.astype(np.int16).copy()\
    result[:, :, 0] = np.clip(result[:, :, 0] + amount, 0, 255)\
    result[:, :, 2] = np.clip(result[:, :, 2] - amount, 0, 255)\
    return result.astype(np.uint8)\
\
\
def lift_shadows(img_array, amount):\
    if amount == 0:\
        return img_array\
    result = img_array.astype(np.float32)\
    darkness = 1 - result / 255.0\
    result = result + darkness * amount\
    return np.clip(result, 0, 255).astype(np.uint8)\
\
\
def cut_highlights(img_array, amount):\
    if amount == 0:\
        return img_array\
    result = img_array.astype(np.float32)\
    brightness_factor = result / 255.0\
    result = result - brightness_factor * amount\
    return np.clip(result, 0, 255).astype(np.uint8)\
\
\
def add_fade(img_array, amount):\
    if amount == 0:\
        return img_array\
    result = img_array.astype(np.float32)\
    result = result * (1 - amount / 100.0) + (amount / 100.0) * 180\
    return np.clip(result, 0, 255).astype(np.uint8)\
\
\
def color_cast(img_array, green=0, red=0, blue_cut=0, cyan=0):\
    result = img_array.astype(np.int16).copy()\
    if red != 0:\
        result[:, :, 0] = np.clip(result[:, :, 0] + red, 0, 255)\
    if green != 0:\
        result[:, :, 1] = np.clip(result[:, :, 1] + green, 0, 255)\
    if blue_cut != 0:\
        result[:, :, 2] = np.clip(result[:, :, 2] - blue_cut, 0, 255)\
    if cyan != 0:\
        result[:, :, 1] = np.clip(result[:, :, 1] + cyan // 2, 0, 255)\
        result[:, :, 2] = np.clip(result[:, :, 2] + cyan, 0, 255)\
    return result.astype(np.uint8)\
\
\
def apply_film_preset(image: Image.Image, preset: dict, custom: dict = None) -> Image.Image:\
    p = \{**preset\}\
    if custom:\
        p.update(custom)\
\
    if p["bw"]:\
        r, g, b = image.split()\
        gray = Image.fromarray(\
            np.clip(\
                np.array(r, dtype=np.float32) * 0.299\
                + np.array(g, dtype=np.float32) * 0.587\
                + np.array(b, dtype=np.float32) * 0.114,\
                0,\
                255,\
            ).astype(np.uint8)\
        )\
        image = gray.convert("RGB")\
    else:\
        sat_enhancer = ImageEnhance.Color(image)\
        image = sat_enhancer.enhance(p["saturation"])\
\
    bright_enhancer = ImageEnhance.Brightness(image)\
    image = bright_enhancer.enhance(p["brightness"])\
\
    contrast_enhancer = ImageEnhance.Contrast(image)\
    image = contrast_enhancer.enhance(p["contrast"])\
\
    arr = np.array(image)\
\
    if not p["bw"]:\
        arr = adjust_warmth(arr, p["warmth"])\
        arr = color_cast(arr, green=p["green_cast"], red=p["red_boost"],\
                         blue_cut=p["blue_cut"], cyan=p["cyan_boost"])\
\
    arr = lift_shadows(arr, p["shadows_lift"])\
    arr = cut_highlights(arr, p["highlight_cut"])\
    arr = add_fade(arr, p["fade"])\
    arr = add_grain(arr, p["grain"])\
    arr = add_vignette(arr, p["vignette"])\
\
    return Image.fromarray(arr)\
\
\
def pil_to_bytes(img: Image.Image, fmt="JPEG", quality=95) -> bytes:\
    buf = io.BytesIO()\
    img.save(buf, format=fmt, quality=quality)\
    return buf.getvalue()\
\
\
st.markdown('<div class="main-title">\uc0\u55357 \u56567  FilmLab</div>', unsafe_allow_html=True)\
st.markdown('<div class="subtitle">\uc0\u49324 \u51652 \u51012  \u50629 \u47196 \u46300 \u54616 \u44256  \u54596 \u47492  \u52852 \u47700 \u46972  \u44048 \u49457 \u51004 \u47196  \u48372 \u51221 \u54644  \u48372 \u49464 \u50836 </div>', unsafe_allow_html=True)\
\
if "selected_preset" not in st.session_state:\
    st.session_state.selected_preset = "Kodak Portra 400"\
\
uploaded_file = st.file_uploader(\
    "\uc0\u49324 \u51652 \u51012  \u46300 \u47000 \u44536 \u54616 \u44144 \u45208  \u53364 \u47533 \u54644 \u49436  \u50629 \u47196 \u46300 ",\
    type=["jpg", "jpeg", "png", "webp"],\
    label_visibility="collapsed",\
)\
\
if uploaded_file:\
    original_image = Image.open(uploaded_file).convert("RGB")\
\
    MAX_SIZE = 1800\
    if max(original_image.size) > MAX_SIZE:\
        ratio = MAX_SIZE / max(original_image.size)\
        new_size = (int(original_image.width * ratio), int(original_image.height * ratio))\
        original_image = original_image.resize(new_size, Image.LANCZOS)\
\
    st.markdown("---")\
    st.markdown('<div class="section-label">\uc0\u54596 \u47492  \u54532 \u47532 \u49483  \u49440 \u53469 </div>', unsafe_allow_html=True)\
\
    preset_names = list(FILM_PRESETS.keys())\
    cols = st.columns(len(preset_names))\
    for i, name in enumerate(preset_names):\
        p = FILM_PRESETS[name]\
        is_selected = st.session_state.selected_preset == name\
        with cols[i]:\
            btn_label = f"\{p['icon']\} \{name\}"\
            if st.button(\
                btn_label,\
                key=f"preset_\{i\}",\
                use_container_width=True,\
                type="primary" if is_selected else "secondary",\
            ):\
                st.session_state.selected_preset = name\
                st.rerun()\
\
    selected = st.session_state.selected_preset\
    preset = FILM_PRESETS[selected]\
\
    st.markdown(f"**\{selected\}** \'97 \{preset['description']\}")\
\
    st.markdown("---")\
    st.markdown('<div class="section-label">\uc0\u49464 \u48512  \u51312 \u51221 </div>', unsafe_allow_html=True)\
\
    adj_col1, adj_col2, adj_col3 = st.columns(3)\
    with adj_col1:\
        adj_brightness = st.slider("\uc0\u48157 \u44592 ", 0.5, 1.8, preset["brightness"], 0.01, key="brightness")\
        adj_contrast = st.slider("\uc0\u45824 \u48708 ", 0.5, 1.8, preset["contrast"], 0.01, key="contrast")\
        adj_saturation = st.slider("\uc0\u52292 \u46020 ", 0.0, 2.0, preset["saturation"], 0.01, key="saturation",\
                                   disabled=preset["bw"])\
    with adj_col2:\
        adj_warmth = st.slider("\uc0\u49353 \u50728 \u46020  (\u46384 \u46907 \u54632 )", -50, 50, preset["warmth"], 1, key="warmth",\
                               disabled=preset["bw"])\
        adj_fade = st.slider("\uc0\u54168 \u51060 \u46300  (\u49353  \u48148 \u47016 )", 0, 40, preset["fade"], 1, key="fade")\
        adj_shadows = st.slider("\uc0\u49744 \u46020 \u50864  \u47532 \u54532 \u53944 ", -10, 40, preset["shadows_lift"], 1, key="shadows")\
    with adj_col3:\
        adj_grain = st.slider("\uc0\u54596 \u47492  \u44536 \u47112 \u51064 ", 0, 60, preset["grain"], 1, key="grain")\
        adj_vignette = st.slider("\uc0\u48708 \u45348 \u54021 ", 0.0, 0.8, preset["vignette"], 0.01, key="vignette")\
        adj_highlight = st.slider("\uc0\u54616 \u51060 \u46972 \u51060 \u53944  \u52983 ", 0, 30, preset["highlight_cut"], 1, key="highlight")\
\
    custom_overrides = \{\
        "brightness": adj_brightness,\
        "contrast": adj_contrast,\
        "saturation": adj_saturation if not preset["bw"] else 0,\
        "warmth": adj_warmth,\
        "fade": adj_fade,\
        "shadows_lift": adj_shadows,\
        "grain": adj_grain,\
        "vignette": adj_vignette,\
        "highlight_cut": adj_highlight,\
    \}\
\
    processed_image = apply_film_preset(original_image, preset, custom_overrides)\
\
    st.markdown("---")\
\
    view_mode = st.radio(\
        "\uc0\u48372 \u44592  \u47784 \u46300 ",\
        ["\uc0\u45208 \u46976 \u55176  \u48708 \u44368 ", "\u50896 \u48376 \u47564 ", "\u48372 \u51221  \u44208 \u44284 \u47564 "],\
        horizontal=True,\
        label_visibility="collapsed",\
    )\
\
    if view_mode == "\uc0\u45208 \u46976 \u55176  \u48708 \u44368 ":\
        img_col1, img_col2 = st.columns(2)\
        with img_col1:\
            st.markdown('<div class="section-label">\uc0\u50896 \u48376 </div>', unsafe_allow_html=True)\
            st.image(original_image, use_container_width=True)\
        with img_col2:\
            st.markdown(f'<div class="section-label">\{selected\}</div>', unsafe_allow_html=True)\
            st.image(processed_image, use_container_width=True)\
    elif view_mode == "\uc0\u50896 \u48376 \u47564 ":\
        st.image(original_image, use_container_width=True)\
    else:\
        st.image(processed_image, use_container_width=True)\
\
    st.markdown("---")\
\
    dl_col1, dl_col2 = st.columns([3, 1])\
    with dl_col1:\
        fmt_choice = st.selectbox("\uc0\u51200 \u51109  \u54805 \u49885 ", ["JPEG (\u44256 \u54868 \u51656 )", "PNG (\u47924 \u49552 \u49892 )"], label_visibility="collapsed")\
    with dl_col2:\
        fmt = "JPEG" if "JPEG" in fmt_choice else "PNG"\
        ext = "jpg" if fmt == "JPEG" else "png"\
        file_data = pil_to_bytes(processed_image, fmt=fmt)\
        st.download_button(\
            label="\uc0\u55357 \u56549  \u45796 \u50868 \u47196 \u46300 ",\
            data=file_data,\
            file_name=f"filmlab_\{selected.replace(' ', '_').lower()\}.\{ext\}",\
            mime=f"image/\{ext\}",\
            use_container_width=True,\
            type="primary",\
        )\
\
else:\
    st.markdown("---")\
    st.markdown("### \uc0\u51648 \u50896 \u54616 \u45716  \u54596 \u47492  \u54532 \u47532 \u49483 ")\
    preset_grid_cols = st.columns(5)\
    for i, (name, p) in enumerate(list(FILM_PRESETS.items())[1:]):\
        with preset_grid_cols[i % 5]:\
            st.markdown(f"**\{p['icon']\} \{name\}**")\
            st.caption(p["description"])\
\
    st.markdown("---")\
    st.info("\uc0\u49324 \u51652 \u51012  \u50629 \u47196 \u46300 \u54616 \u47732  \u45796 \u50577 \u54620  \u54596 \u47492  \u52852 \u47700 \u46972  \u54532 \u47532 \u49483 \u51012  \u51201 \u50857 \u54616 \u44256  \u45796 \u50868 \u47196 \u46300 \u54624  \u49688  \u51080 \u49845 \u45768 \u45796 .")\
}