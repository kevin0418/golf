

### 개선된 코드

import streamlit as st
import geocoder

from geopy.distance import geodesic

# Jindalee Golf Course 홀컵 좌표 (위도, 경도)
HOLE_COORDS = {
    1: (-27.53918, 152.945457),
    2: (-27.53658, 152.94362),
    3: (-27.536325, 152.946275),
    4: (-27.535989, 152.943866),
    5: (-27.534852, 152.944261),
    6: (-27.532689, 152.945452),
    7: (-27.534462, 152.944352),
    8: (-27.532874, 152.943498),
    9: (-27.535837, 152.943191),
    10: (-27.53918, 152.945457),
    11: (-27.53658, 152.94362),
    12: (-27.536325, 152.946275),
    13: (-27.535989, 152.943866),
    14: (-27.534852, 152.944261),
    15: (-27.532689, 152.945452),
    16: (-27.534462, 152.944352),
    17: (-27.532874, 152.943498),
    18: (-27.535837, 152.943191)
}


# Streamlit UI
# st.title("🏌️ Jindalee Golf Course 홀 거리 측정")
st.markdown("#### Jindalee Golf Course :red[홀 거리] by Kevin")
st.markdown("현 위치에서  홀컵까지 거리 계산")

# 홀 선택
hole_number = st.selectbox(
    "홀 번호  선택 (1-18):",
    options=list(range(1, 19)),
    index=0
)

# 현재 위치를 찾기
g = geocoder.ip('me')

# 위도와 경도 출력
current_lat = g.latlng[0]
current_lon = g.latlng[1]

current_pos = (current_lat, current_lon)

# st.button("거리 계산", type="primary")  # 기본 테마 색상
# st.button("거리 계산", type="secondary")  # 보조 색상
# 거리 계산
if st.button("거리 계산", type="secondary"):
    if hole_number in HOLE_COORDS:
        target_pos = HOLE_COORDS[hole_number]
        distance_m = geodesic(current_pos, target_pos).meters
        distance_yard = distance_m * 1.09361  # 미터 → 야드 변환
        
        st.success(
            f"**홀 {hole_number}까지 거리:**\n\n"
            f"- {distance_m:.2f} 미터\n"
        #    f"- {distance_yard:.2f} 야드"
        )
        
        # 추가 시각화 (선택 사항)
        st.progress(min(1.0, distance_m / 300))  # 300m를 최대 기준으로 진행률 표시
    else:
        st.error("유효하지 않은 홀 번호입니다.")


#