# 

import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from streamlit_geolocation import streamlit_geolocation

def main():
    st.title('모바일 GPS 위치 추적기 by Kevin')

    # 위치 정보 가져오기
    location = streamlit_geolocation()
    
    if location:
        lat = location.get('latitude')
        lon = location.get('longitude')
        
        if lat and lon:
            # 지도 생성
            m = folium.Map(location=[lat, lon], zoom_start=15)
            
            # 현재 위치 마커 추가
            folium.Marker(
                [lat, lon],
                popup='현재 위치',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

            # 지도 표시
            folium_static(m)

            # 주소 정보 표시
            try:
                geolocator = Nominatim(user_agent="my_app")
                location = geolocator.reverse(f"{lat}, {lon}")
                st.write(f"현재 주소: {location.address}")
            except Exception as e:
                st.warning(f"주소를 가져오는 데 실패했습니다: {e}")

if __name__ == "__main__":
    main()