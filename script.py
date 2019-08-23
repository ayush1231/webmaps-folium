import folium
import pandas
import json

data = pandas.read_csv("Volcanoes_USA.txt")

lat = list(data.LAT)
lon = list(data.LON)
elev = list(data.ELEV)
name = list(data.NAME)

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q={}" target="_blank">{}</a><br>
Height: {} m
"""


def color_mapping(elevation):

    if elevation < 1000:
        return 'green'

    elif 1000 <= elevation < 3000:
        return 'orange'

    else:
        return 'red'


map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles='Stamen Terrain')


fg_volcano = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, name in zip(lat, lon, elev, name):

    iframe = folium.IFrame(html=html.format(name, name, el), width=200, height=100)

    #fg_volcano.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe),
    #                          fill_color=color_mapping(el), icon=folium.Icon(color=color_mapping(el))))

    fg_volcano.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe),   fill_color=color_mapping(el), color='grey', fill_opacity=0.7))


fg_population = folium.FeatureGroup("Population")

fg_population.add_child(folium.GeoJson(json.load(open("world.json", "r", encoding="utf-8-sig")),
                            style_function=lambda x: {'fillColor':'green' if x["properties"]["POP2005"] < 10000000
                            else 'orange' if 10000000 <= x['properties']['POP2005'] <= 20000000 else 'red'}))


map.add_child(fg_volcano)
map.add_child(fg_population)

map.add_child(folium.LayerControl())
map.save("map1.html")
