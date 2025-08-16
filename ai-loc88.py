import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
from geopy.geocoders import Nominatim

def main():
    st.title('모바일 GPS 위치 추적기')

    # JavaScript를 사용하여 위치 정보 가져오기
    st.markdown(
        """
        <script>
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                window.parent.postMessage({
                    'type': 'location',
                    'latitude': latitude,
                    'longitude': longitude
                }, '*');
            });
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    # 위치 정보를 보여줄 지도 생성
    if 'latitude' in st.session_state and 'longitude' in st.session_state:
        lat = st.session_state.latitude
        lon = st.session_state.longitude

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
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.reverse(f"{lat}, {lon}")
        st.write(f"현재 주소: {location.address}")

if __name__ == "__main__":
    main()
