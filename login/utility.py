import geocoder
import re
def get_location_info(latitude, longitude):
    location = geocoder.osm([latitude, longitude], method='reverse')
    
    if location.ok:
        city = location.city
        state = location.state
        postal = location.postal
        country = location.country
        return city, state, postal, country
    else:
        return None, None, None, None

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def emailCheck(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False