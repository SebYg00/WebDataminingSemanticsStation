from flask import Flask
import folium
import json
import requests

app = Flask(__name__)

@app.route("/")
def base():
    name = input("Choose a city : ")
    if(name=='Rennes'):
        map = folium.Map(
            location=[48.1, -1.6777926],
            tiles='Stamen Terrain',
            zoom_start=13
        )
    elif(name=="Strasbourg"):
        map = folium.Map(
            location=[48.5734053, 7.7521113],
            tiles='Stamen Terrain',
            zoom_start=13
        )
    elif(name=="Lyon"):
        map = folium.Map(
            location=[45.75, 4.849664],
            tiles='Stamen Terrain',
            zoom_start=12
        )
    elif(name=="Montpellier"):
        map = folium.Map(
            location=[43.605, 3.876716],
            tiles='Stamen Terrain',
            zoom_start=14
        )

    tmp = []
    #RENNES
    rennes = requests.get('https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel')
    rennes = rennes.json()
    rennes = rennes['records']
    for i in range(len(rennes)):
        tmp.append({'name': rennes[i]['fields']['nom'],
        'lat':rennes[i]['fields']['coordonnees'][0],
        'lon':rennes[i]['fields']['coordonnees'][1],
        'available_place':rennes[i]['fields']['nombrevelosdisponibles']})
    #STRASBOURG
    strasbourg = json.load(open('strasbourg.json'))
    strasbourg = strasbourg['vcs']['sl']['si']
    for i in range(len(strasbourg)):
        tmp.append({'name': strasbourg[i]['-na'],
        'lat':strasbourg[i]['-la'],
        'lon':strasbourg[i]['-lg'],
        'available_place':strasbourg[i]['-av']})
    #LYON
    lyon = requests.get("https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171")
    lyon = lyon.json()
    lyon = lyon['features']
    for i in range(len(lyon)):
        tmp.append({'name' : lyon[i]['properties']['name'],  
        'lat' : float(lyon[i]['properties']['lat']), 
        'lon' : float(lyon[i]['properties']['lng']),
        'available_place':lyon[i]['properties']['available_bike_stands']})
    #MONTPELLIER
    montpellier = json.load(open('montpellier.json'))
    montpellier = montpellier['vcs']['sl']['si']
    for i in range(len(montpellier)):
        tmp.append({'name': montpellier[i]['-na'],
        'lat':montpellier[i]['-la'],
        'lon':montpellier[i]['-lg'],
        'available_place':montpellier[i]['-av']})

    


    for i in range(len(tmp)):
            folium.Marker(
                location=[tmp[i]['lat'], tmp[i]['lon']],
                popup="Emplacement(s) disponible(s) : {}".format(tmp[i]['available_place']),
                tooltip=tmp[i]['name']
            ).add_to(map)   

    return map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)