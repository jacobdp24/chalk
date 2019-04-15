class location():
    def __init__(self, lat, lng, name, id):
        self.hotspot = {
        'id' : id,
        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'lat': lat,
        'lng': lng,
        'infobox': f"<a href='http://127.0.0.1:8080/location/{id}'>{name}</a>",
        'name': name
        }
