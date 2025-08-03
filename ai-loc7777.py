# Jindalee Golf Course GPS 거리 측정 앱 (모바일 GPS 지원)
# Jindalee Golf Course GPS 거리 측정 앱 (Android 호환)
import streamlit as st
from geopy.distance import geodesic
import time

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

def get_geolocation():
    """Android에서 안정적인 위치 정보 가져오기"""
    try:
        # Streamlit의 내장 위치 기능 사용
        return st.gps()
    except Exception as e:
        st.warning(f"위치 서비스 오류: {str(e)}")
        return None

def main():
    st.markdown("#### :red[홀 거리 측정] by Kevin")
    st.markdown("현재 위치에서 홀컵까지의 거리를 계산합니다")
    
    # 세션 상태 초기화
    if 'current_pos' not in st.session_state:
        st.session_state.current_pos = None
        st.session_state.location_retry = 0
    
    # 위치 서비스 요청 섹션
    st.subheader("📍 위치 서비스")
    
    # 위치 요청 버튼
    if st.button("현재 위치 가져오기", type="primary"):
        with st.spinner("위치 정보 수신 중..."):
            location = None
            retry_count = 0
            
            # 최대 3회 재시도
            while not location and retry_count < 3:
                location = get_geolocation()
                retry_count += 1
                if not location:
                    time.sleep(1)  # 재시도 전 대기
            
            if location:
                lat = location.get("latitude")
                lon = location.get("longitude")
                
                if lat is not None and lon is not None:
                    st.session_state.current_pos = (lat, lon)
                    st.success(f"위치 갱신 성공! 위도: {lat:.6f}, 경도: {lon:.6f}")
                    st.map([st.session_state.current_pos], zoom=16)
                else:
                    st.warning("위치 정보를 가져오지 못했습니다. 위치 서비스가 활성화되었는지 확인하세요.")
            else:
                st.warning("위치 정보를 가져오지 못했습니다. 수동으로 입력해주세요.")
    
    # 수동 입력 폼
    st.markdown("**수동 위치 입력 (선택사항)**")
    with st.form("manual_location"):
        col1, col2 = st.columns(2)
        with col1:
            manual_lat = st.text_input("위도", value="-27.53918")
        with col2:
            manual_lon = st.text_input("경도", value="152.945457")
        
        submit_manual = st.form_submit_button("수동 위치 적용")
        
        if submit_manual:
            try:
                lat = float(manual_lat)
                lon = float(manual_lon)
                st.session_state.current_pos = (lat, lon)
                st.success(f"수동 위치 적용됨: 위도 {lat:.6f}, 경도 {lon:.6f}")
            except ValueError:
                st.error("유효한 숫자를 입력해주세요")

    # 거리 계산 섹션
    st.subheader("🏌️ 홀 거리 계산")
    hole_number = st.selectbox(
        "홀 번호 선택 (1-18):",
        options=list(range(1, 19)),
        index=0
    )
    
    if st.button("거리 계산", type="primary"):
        if st.session_state.current_pos is None:
            st.error("먼저 위치 정보를 가져오거나 입력해주세요.")
        elif hole_number in HOLE_COORDS:
            target_pos = HOLE_COORDS[hole_number]
            
            try:
                distance_m = geodesic(st.session_state.current_pos, target_pos).meters
                
                # 거리 시각화
                st.success(
                    f"**홀 {hole_number}까지 거리:**\n\n"
                    f"- {distance_m:.2f} 미터\n"
                    f"- {distance_m * 1.09361:.2f} 야드"
                )
                
                # 거리 진행률 표시
                max_distance = 300
                progress = min(1.0, distance_m / max_distance)
                st.progress(progress)
                st.caption(f"기준 거리: {max_distance}m (진행률 {progress*100:.0f}%)")
                
                # 지도 시각화
                st.map(
                    [st.session_state.current_pos, target_pos],
                    zoom=15,
                    color=['#FF0000', '#0000FF']  # 빨강: 현재 위치, 파랑: 홀 위치
                )
            except Exception as e:
                st.error(f"거리 계산 오류: {str(e)}")
        else:
            st.error("유효하지 않은 홀 번호입니다.")

if __name__ == '__main__':
    st.set_page_config(
        page_title="Jindalee Golf GPS",
        page_icon="⛳",
        layout="centered"
    )
    main()


# # Jindalee Golf Course GPS 거리 측정 앱 (모바일 GPS 지원)
# #

# import streamlit as st
# from geopy.distance import geodesic
# from streamlit_geolocation import streamlit_geolocation

# # Jindalee Golf Course 홀컵 좌표 (위도, 경도)
# HOLE_COORDS = {
#     1: (-27.53918, 152.945457),
#     2: (-27.53658, 152.94362),
#     3: (-27.536325, 152.946275),
#     4: (-27.535989, 152.943866),
#     5: (-27.534852, 152.944261),
#     6: (-27.532689, 152.945452),
#     7: (-27.534462, 152.944352),
#     8: (-27.532874, 152.943498),
#     9: (-27.535837, 152.943191),
#     10: (-27.53918, 152.945457),
#     11: (-27.53658, 152.94362),
#     12: (-27.536325, 152.946275),
#     13: (-27.535989, 152.943866),
#     14: (-27.534852, 152.944261),
#     15: (-27.532689, 152.945452),
#     16: (-27.534462, 152.944352),
#     17: (-27.532874, 152.943498),
#     18: (-27.535837, 152.943191)
# }

# def main():
#     st.markdown("#### :red[홀 거리 측정] by Kevin")
#     st.markdown("현재 위치에서 홀컵까지의 거리를 계산합니다")
    
#     # 세션 상태 초기화
#     if 'current_pos' not in st.session_state:
#         st.session_state.current_pos = None
    
#     # 위치 서비스 요청 섹션
#     st.subheader("📍 위치 서비스")
#     st.markdown("**1. 현재 위치 가져오기**")
    
#     # 위치 요청 버튼
#     location = streamlit_geolocation()
    
#     # 위치 정보 처리 - None 값 체크 추가
#     if location and 'latitude' in location and 'longitude' in location:
#         lat = location['latitude']
#         lon = location['longitude']
        
#         # 위치 정보가 유효한 경우에만 처리
#         if lat is not None and lon is not None:
#             st.session_state.current_pos = (lat, lon)
#             st.success(f"위치 갱신 성공! 위도: {lat:.6f}, 경도: {lon:.6f}")
#             st.map([st.session_state.current_pos], zoom=16)
#         else:
#             st.warning("위치 정보를 가져오지 못했습니다. 위치 서비스가 활성화되었는지 확인하세요.")
#     else:
#         st.warning("위치 정보를 가져오지 못했습니다. 수동으로 입력하세요.")
    
#     # 수동 입력 폼
#     st.markdown("**2. 수동 위치 입력 (선택사항)**")
#     with st.form("manual_location"):
#         manual_lat = st.text_input("위도", value="-27.53918")
#         manual_lon = st.text_input("경도", value="152.945457")
#         submit_manual = st.form_submit_button("수동 위치 적용")
        
#         if submit_manual:
#             try:
#                 lat = float(manual_lat)
#                 lon = float(manual_lon)
#                 st.session_state.current_pos = (lat, lon)
#                 st.success(f"수동 위치 적용됨: 위도 {lat:.6f}, 경도 {lon:.6f}")
#             except ValueError:
#                 st.error("유효한 숫자를 입력해주세요")

#     # 거리 계산 섹션
#     st.subheader("🏌️ 홀 거리 계산")
#     hole_number = st.selectbox(
#         "홀 번호 선택 (1-18):",
#         options=list(range(1, 19)),
#         index=0
#     )
    
#     if st.button("거리 계산", type="primary"):
#         if st.session_state.current_pos is None:
#             st.error("먼저 위치 정보를 가져오거나 입력해주세요.")
#         elif hole_number in HOLE_COORDS:
#             target_pos = HOLE_COORDS[hole_number]
#             distance_m = geodesic(st.session_state.current_pos, target_pos).meters
            
#             # 거리 시각화
#             st.success(
#                 f"**홀 {hole_number}까지 거리:**\n\n"
#                 f"- {distance_m:.2f} 미터\n"
#                 f"- {distance_m * 1.09361:.2f} 야드"
#             )
            
#             # 거리 진행률 표시
#             max_distance = 300
#             progress = min(1.0, distance_m / max_distance)
#             st.progress(progress)
#             st.caption(f"기준 거리: {max_distance}m (진행률 {progress*100:.0f}%)")
            
#             # 지도 시각화
#             st.map(
#                 [st.session_state.current_pos, target_pos],
#                 zoom=15,
#                 color=['#FF0000', '#0000FF']  # 빨강: 현재 위치, 파랑: 홀 위치
#             )
#         else:
#             st.error("유효하지 않은 홀 번호입니다.")

# if __name__ == '__main__':
#     main()

#

# import streamlit as st
# from geopy.distance import geodesic
# from streamlit_geolocation import streamlit_geolocation

# # Jindalee Golf Course 홀컵 좌표 (위도, 경도)
# HOLE_COORDS = {
#     1: (-27.53918, 152.945457),
#     2: (-27.53658, 152.94362),
#     3: (-27.536325, 152.946275),
#     4: (-27.535989, 152.943866),
#     5: (-27.534852, 152.944261),
#     6: (-27.532689, 152.945452),
#     7: (-27.534462, 152.944352),
#     8: (-27.532874, 152.943498),
#     9: (-27.535837, 152.943191),
#     10: (-27.53918, 152.945457),
#     11: (-27.53658, 152.94362),
#     12: (-27.536325, 152.946275),
#     13: (-27.535989, 152.943866),
#     14: (-27.534852, 152.944261),
#     15: (-27.532689, 152.945452),
#     16: (-27.534462, 152.944352),
#     17: (-27.532874, 152.943498),
#     18: (-27.535837, 152.943191)
# }

# def main():
#     st.markdown("#### :red[홀 거리 측정] by Kevin")
#     st.markdown("현재 위치에서 홀컵까지의 거리를 계산합니다")
    
#     # 세션 상태 초기화
#     if 'current_pos' not in st.session_state:
#         st.session_state.current_pos = None
    
#     # 위치 서비스 요청 섹션
#     st.subheader("📍 위치 서비스")
#     st.markdown("**1. 현재 위치 가져오기**")
    
#     # 위치 요청 버튼
#     location = streamlit_geolocation()
    
#     # 위치 정보 처리
#     if location and 'latitude' in location and 'longitude' in location:
#         lat = location['latitude']
#         lon = location['longitude']
#         st.session_state.current_pos = (lat, lon)
#         st.success(f"위치 갱신 성공! 위도: {lat:.6f}, 경도: {lon:.6f}")
#         st.map([st.session_state.current_pos], zoom=16)
#     else:
#         st.warning("위치 정보를 가져오지 못했습니다. 수동으로 입력하세요.")
    
#     # 수동 입력 폼
#     st.markdown("**2. 수동 위치 입력 (선택사항)**")
#     with st.form("manual_location"):
#         manual_lat = st.text_input("위도", value="-27.53918")
#         manual_lon = st.text_input("경도", value="152.945457")
#         submit_manual = st.form_submit_button("수동 위치 적용")
        
#         if submit_manual:
#             try:
#                 lat = float(manual_lat)
#                 lon = float(manual_lon)
#                 st.session_state.current_pos = (lat, lon)
#                 st.success(f"수동 위치 적용됨: 위도 {lat:.6f}, 경도 {lon:.6f}")
#             except ValueError:
#                 st.error("유효한 숫자를 입력해주세요")

#     # 거리 계산 섹션
#     st.subheader("🏌️ 홀 거리 계산")
#     hole_number = st.selectbox(
#         "홀 번호 선택 (1-18):",
#         options=list(range(1, 19)),
#         index=0
#     )
    
#     if st.button("거리 계산", type="primary"):
#         if st.session_state.current_pos is None:
#             st.error("먼저 위치 정보를 가져오거나 입력해주세요.")
#         elif hole_number in HOLE_COORDS:
#             target_pos = HOLE_COORDS[hole_number]
#             distance_m = geodesic(st.session_state.current_pos, target_pos).meters
            
#             # 거리 시각화
#             st.success(
#                 f"**홀 {hole_number}까지 거리:**\n\n"
#                 f"- {distance_m:.2f} 미터\n"
#                 f"- {distance_m * 1.09361:.2f} 야드"
#             )
            
#             # 거리 진행률 표시
#             max_distance = 300
#             progress = min(1.0, distance_m / max_distance)
#             st.progress(progress)
#             st.caption(f"기준 거리: {max_distance}m (진행률 {progress*100:.0f}%)")
            
#             # 지도 시각화
#             st.map(
#                 [st.session_state.current_pos, target_pos],
#                 zoom=15,
#                 color=['#FF0000', '#0000FF']  # 빨강: 현재 위치, 파랑: 홀 위치
#             )
#         else:
#             st.error("유효하지 않은 홀 번호입니다.")

# if __name__ == '__main__':
#     main()