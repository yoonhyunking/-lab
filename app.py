import io
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance

st.set_page_config(
    page_title="FilmLab",
    page_icon="📷",
    layout="wide",
)

st.markdown("""
<style>
div[data-testid="stImage"] img { border-radius: 10px; }
.stButton > button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

PRESETS = {
    "원본": dict(brightness=1.0, contrast=1.0, saturation=1.0,
                 warmth=0, shadows=0, highlights=0,
                 grain=0, vignette=0.0, fade=0, bw=False,
                 r=0, g=0, b=0, icon="🖼️",
                 desc="보정 없이 원본 그대로"),
    "Kodak Portra 400": dict(brightness=1.08, contrast=0.92, saturation=0.88,
                              warmth=18, shadows=12, highlights=8,
                              grain=18, vignette=0.18, fade=10, bw=False,
                              r=10, g=4, b=-8, icon="🌅",
                              desc="따뜻하고 자연스러운 스킨톤, 인물 사진에 최적"),
    "Kodak Gold 200": dict(brightness=1.05, contrast=1.05, saturation=1.15,
                            warmth=25, shadows=8, highlights=5,
                            grain=22, vignette=0.22, fade=8, bw=False,
                            r=18, g=6, b=-14, icon="☀️",
                            desc="황금빛 여름 느낌, 빈티지 감성"),
    "Fuji Velvia 50": dict(brightness=1.0, contrast=1.18, saturation=1.45,
                            warmth=-6, shadows=0, highlights=10,
                            grain=8, vignette=0.14, fade=0, bw=False,
                            r=0, g=12, b=10, icon="🌿",
                            desc="선명하고 채도 높은 자연 풍경용"),
    "Fuji Pro 400H": dict(brightness=1.12, contrast=0.88, saturation=0.80,
                           warmth=-10, shadows=18, highlights=12,
                           grain=14, vignette=0.12, fade=16, bw=False,
                           r=-5, g=8, b=12, icon="🌸",
                           desc="파스텔 톤, 부드럽고 청량한 느낌"),
    "Ilford HP5 (흑백)": dict(brightness=1.0, contrast=1.15, saturation=0.0,
                               warmth=0, shadows=5, highlights=5,
                               grain=28, vignette=0.28, fade=5, bw=True,
                               r=0, g=0, b=0, icon="⬛",
                               desc="클래식 흑백, 강한 대비와 깊이"),
    "Kodak T-MAX (흑백)": dict(brightness=1.04, contrast=1.08, saturation=0.0,
                                warmth=0, shadows=10, highlights=8,
                                grain=14, vignette=0.20, fade=8, bw=True,
                                r=0, g=0, b=0, icon="🌑",
                                desc="세밀한 그레인, 부드러운 흑백"),
    "Agfa Vista (페이드)": dict(brightness=1.06, contrast=0.85, saturation=0.75,
                                 warmth=12, shadows=22, highlights=8,
                                 grain=24, vignette=0.30, fade=25, bw=False,
                                 r=8, g=10, b=-5, icon="📼",
                                 desc="빈티지 색 바램, 레트로 감성"),
    "Lomo LC-A": dict(brightness=0.95, contrast=1.25, saturation=1.35,
                       warmth=8, shadows=0, highlights=15,
                       grain=30, vignette=0.55, fade=0, bw=False,
                       r=12, g=0, b=0, icon="🔮",
                       desc="강한 비네팅과 채도, 로모그래피 스타일"),
    "Cross Process": dict(brightness=1.05, contrast=1.30, saturation=1.40,
                           warmth=-15, shadows=0, highlights=20,
                           grain=20, vignette=0.25, fade=0, bw=False,
                           r=15, g=20, b=15, icon="🎨",
                           desc="슬라이드 필름 교차 현상, 강렬한 색상 왜곡"),
}


def to_array(img: Image.Image) -> np.ndarray:
    return np.array(img, dtype=np.float32)


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def apply_bw(img: Image.Image) -> Image.Image:
    arr = to_array(img)
    gray = arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114
    arr[:, :, 0] = gray
    arr[:, :, 1] = gray
    arr[:, :, 2] = gray
    return to_image(arr)


def apply_warmth(arr: np.ndarray, amount: int) -> np.ndarray:
    if amount == 0:
        return arr
    arr = arr.copy()
    arr[:, :, 0] = np.clip(arr[:, :, 0] + amount, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] - amount, 0, 255)
    return arr


def apply_color_shift(arr: np.ndarray, r: int, g: int, b: int) -> np.ndarray:
    if r == 0 and g == 0 and b == 0:
        return arr
    arr = arr.copy()
    arr[:, :, 0] = np.clip(arr[:, :, 0] + r, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + g, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + b, 0, 255)
    return arr


def apply_shadows(arr: np.ndarray, amount: int) -> np.ndarray:
    if amount == 0:
        return arr
    darkness = 1.0 - arr / 255.0
    return np.clip(arr + darkness * amount, 0, 255)


def apply_highlights(arr: np.ndarray, amount: int) -> np.ndarray:
    if amount == 0:
        return arr
    brightness = arr / 255.0
    return np.clip(arr - brightness * amount, 0, 255)


def apply_fade(arr: np.ndarray, amount: int) -> np.ndarray:
    if amount == 0:
        return arr
    t = amount / 100.0
    return arr * (1 - t) + 180.0 * t


def apply_grain(arr: np.ndarray, intensity: int) -> np.ndarray:
    if intensity == 0:
        return arr
    rng = np.random.default_rng(seed=42)
    noise = rng.normal(0, intensity, arr.shape)
    return np.clip(arr + noise, 0, 255)


def apply_vignette(arr: np.ndarray, strength: float) -> np.ndarray:
    if strength == 0:
        return arr
    h, w = arr.shape[:2]
    cy, cx = h / 2, w / 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
    dist = dist / dist.max()
    mask = 1.0 - (dist ** 1.5) * strength
    mask = np.clip(mask, 0, 1)[:, :, np.newaxis]
    return np.clip(arr * mask, 0, 255)


def process(image: Image.Image, p: dict) -> Image.Image:
    if p["bw"]:
        image = apply_bw(image)
    else:
        image = ImageEnhance.Color(image).enhance(p["saturation"])

    image = ImageEnhance.Brightness(image).enhance(p["brightness"])
    image = ImageEnhance.Contrast(image).enhance(p["contrast"])

    arr = to_array(image)

    if not p["bw"]:
        arr = apply_warmth(arr, p["warmth"])
        arr = apply_color_shift(arr, p["r"], p["g"], p["b"])

    arr = apply_shadows(arr, p["shadows"])
    arr = apply_highlights(arr, p["highlights"])
    arr = apply_fade(arr, p["fade"])
    arr = apply_grain(arr, p["grain"])
    arr = apply_vignette(arr, p["vignette"])

    return to_image(arr)


def img_to_bytes(img: Image.Image, fmt: str = "JPEG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt, quality=95)
    return buf.getvalue()


st.title("📷 FilmLab")
st.caption("사진을 업로드하고 필름 카메라 감성으로 보정해 보세요")

uploaded = st.file_uploader(
    "JPG, PNG, WEBP 파일 업로드",
    type=["jpg", "jpeg", "png", "webp"],
)

if not uploaded:
    st.markdown("---")
    st.subheader("지원하는 필름 프리셋")
    cols = st.columns(5)
    for i, (name, p) in enumerate(list(PRESETS.items())[1:]):
        with cols[i % 5]:
            st.markdown(f"**{p['icon']} {name}**")
            st.caption(p["desc"])
    st.stop()

original = Image.open(uploaded).convert("RGB")
MAX = 1800
if max(original.size) > MAX:
    r = MAX / max(original.size)
    original = original.resize(
        (int(original.width * r), int(original.height * r)), Image.LANCZOS
    )

st.markdown("---")
st.subheader("필름 프리셋")

if "preset" not in st.session_state:
    st.session_state.preset = "Kodak Portra 400"

preset_names = list(PRESETS.keys())
btn_cols = st.columns(len(preset_names))
for i, name in enumerate(preset_names):
    p = PRESETS[name]
    is_sel = st.session_state.preset == name
    with btn_cols[i]:
        if st.button(
            f"{p['icon']} {name}",
            key=f"btn_{i}",
            use_container_width=True,
            type="primary" if is_sel else "secondary",
        ):
            st.session_state.preset = name
            st.rerun()

sel = st.session_state.preset
preset = PRESETS[sel]
st.caption(f"**{sel}** — {preset['desc']}")

st.markdown("---")
st.subheader("세부 조정")

c1, c2, c3 = st.columns(3)
with c1:
    brightness = st.slider("밝기", 0.5, 1.8, float(preset["brightness"]), 0.01)
    contrast   = st.slider("대비", 0.5, 1.8, float(preset["contrast"]), 0.01)
    saturation = st.slider("채도", 0.0, 2.0, float(preset["saturation"]), 0.01,
                           disabled=preset["bw"])
with c2:
    warmth     = st.slider("색온도 (따뜻함)", -50, 50, int(preset["warmth"]), 1,
                           disabled=preset["bw"])
    fade       = st.slider("페이드 (색 바램)", 0, 40, int(preset["fade"]), 1)
    shadows    = st.slider("쉐도우 리프트", -10, 40, int(preset["shadows"]), 1)
with c3:
    grain      = st.slider("필름 그레인", 0, 60, int(preset["grain"]), 1)
    vignette   = st.slider("비네팅", 0.0, 0.8, float(preset["vignette"]), 0.01)
    highlights = st.slider("하이라이트 컷", 0, 30, int(preset["highlights"]), 1)

params = {
    **preset,
    "brightness": brightness,
    "contrast":   contrast,
    "saturation": 0.0 if preset["bw"] else saturation,
    "warmth":     0   if preset["bw"] else warmth,
    "fade":       fade,
    "shadows":    shadows,
    "grain":      grain,
    "vignette":   vignette,
    "highlights": highlights,
}

result = process(original, params)

st.markdown("---")
view = st.radio(
    "보기 모드",
    ["나란히 비교", "원본만", "보정 결과만"],
    horizontal=True,
    label_visibility="collapsed",
)

if view == "나란히 비교":
    l, r_col = st.columns(2)
    with l:
        st.caption("원본")
        st.image(original, use_container_width=True)
    with r_col:
        st.caption(sel)
        st.image(result, use_container_width=True)
elif view == "원본만":
    st.image(original, use_container_width=True)
else:
    st.image(result, use_container_width=True)

st.markdown("---")
d1, d2 = st.columns([3, 1])
with d1:
    fmt_choice = st.selectbox("저장 형식", ["JPEG (고화질)", "PNG (무손실)"],
                              label_visibility="collapsed")
with d2:
    fmt = "JPEG" if "JPEG" in fmt_choice else "PNG"
    ext = "jpg" if fmt == "JPEG" else "png"
    st.download_button(
        label="📥 다운로드",
        data=img_to_bytes(result, fmt),
        file_name=f"filmlab_{sel.replace(' ', '_').lower()}.{ext}",
        mime=f"image/{ext}",
        use_container_width=True,
        type="primary",
    )
