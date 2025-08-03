#
#  Deep Seek 작업 
#

import streamlit as st
import random
import time
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

# Streamlit 앱

#gps = (lat, lon)

def main():
    # st.title("🏌️ Jindalee Golf Course GPS 거리 측정")
    # st.markdown("### Jindalee Golf Course GPS 거리 측정")
    st.markdown("#### :red[홀 거리 측정] by Kevin")
    st.markdown("현재 위치에서 홀컵까지의 거리를 계산합니다")
    
    # 세션 상태 초기화
    if 'current_pos' not in st.session_state:
        st.session_state.current_pos = None
    
# 위도와 경도 입력 받기
    # lat = st.text_input("현위치 위도 입력", "")
    # lon = st.text_input("현위치 경도 입력", "")
    lat, lon = st.text_input('현위치 위도 입력', '-27.60'), st.text_input('현위치 경도 입력', '152.94')

# 입력값이 유효한지 확인
    if lat and lon: 
        try:
             lat = float(lat)
             lon = float(lon)
             st.session_state.current_pos = (lat, lon)
             st.success(f"위도: {lat}, 경도: {lon}")
        except ValueError:
             st.error("숫자가 아닌 값을 입력했습니다.")

    # 거리 계산 섹션
    st.subheader(" 홀 거리 계산")
    hole_number = st.selectbox(
        "홀 번호 선택 (1-18):",
        options=list(range(1, 19)),
        index=0
    )
    
    #gps = DummyGPS()

    if st.button("거리 계산", type="secondary"):
        if st.session_state.current_pos is None:
            st.error("먼저 '위치 측정' 버튼으로 현재 위치를 확인해주세요.")
        elif hole_number in HOLE_COORDS:
            target_pos = HOLE_COORDS[hole_number]
            distance_m = geodesic(st.session_state.current_pos, target_pos).meters
            
            st.success(
                f"**홀 {hole_number}까지 거리:**\n\n"
                f"- {distance_m:.2f} 미터\n"
                f"- {distance_m * 1.09361:.2f} 야드"
            )
            
            # 추가 시각화
            max_distance = 300  # 진행률 표시 기준 (300m)
            progress = min(1.0, distance_m / max_distance)
            st.progress(progress)
            st.caption(f"기준 거리: {max_distance}m (진행률 {progress*100:.0f}%)")
        else:
            st.error("유효하지 않은 홀 번호입니다.")

if __name__ == '__main__':
    main()
