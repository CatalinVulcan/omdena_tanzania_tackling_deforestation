import streamlit as st
import folium
from streamlit_folium import folium_static
import json

def main():

    st.set_page_config(layout='centered')
    
    # Page styling
    st.markdown(f"""
        <style>
            .css-1y4p8pa {{
                padding: 0
            }}
        </style>""",
        unsafe_allow_html=True,
    )

    st.title("Forest Loss over the years")
    year = st.selectbox("Loss Year", (2017, 2018, 2019, 2020, 2021, 2022))

    # Create a Folium map centered on rufiji delta
    m = folium.Map(location=[-7.8277, 39.2973],
                   zoom_start=12)
    
    style = {'fillColor': '#FF0000', 'fillOpacity': .4, 'color': '#FF0000', 'weight': 1}
    style_GMW = {'fillColor': '#000090', 'fillOpacity': .4, 'color': '#000090', 'weight': 1}
    style_GFW = {'fillColor': 'green', 'fillOpacity': .4, 'color': 'green', 'weight': 1}

    @st.cache_data
    def load_shapefile(year, origin):
        return json.load(
                open(f"./loss areas/{origin}/{year}.geojson", encoding="utf8")
        )

    folium.GeoJson(
        load_shapefile(year, origin="Ours"),
        style_function=lambda x: style,
        name="Deforestation"
    ).add_to(m)

    folium.GeoJson(
        load_shapefile(year, origin="GFW"),
        style_function=lambda x: style_GFW,
        name="GFW Deforestation"
    ).add_to(m)

    if (year>=2017) & (year<=2020):
        folium.GeoJson(
            load_shapefile(year, origin="GMW"),
            style_function=lambda x: style_GMW,
            name="GMW Deforestation"
        ).add_to(m)

    folium.LayerControl().add_to(m)

    # Display the map in Streamlit
    folium_static(m, width=736)


if __name__ == '__main__':
    main()
