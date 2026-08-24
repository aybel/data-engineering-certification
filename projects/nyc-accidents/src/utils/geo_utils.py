

def localidad(lat,lon):
    """
        Funcion que regresa la localidad mas probable
        dependiendo de una latitud y longitud dada
    """
    geolocator = Nominatim(user_agent="mi_aplicacion_geolocalizacion")
    
    # Combinar latitud y longitud en formato de cadena o tupla
    coordenadas = f"{latitud}, {longitud}"
    
    # Obtener la ubicación
    ubicacion = geolocator.reverse(coordenadas, language='es')
    
    if ubicacion and ubicacion.raw.get('address'):
        direccion = ubicacion.raw['address']
        # Buscar localidad, ciudad, pueblo o municipio en orden de prioridad
        localidad = (
            direccion.get('city') or 
            direccion.get('town') or 
            direccion.get('village') or 
            direccion.get('municipality') or 
            direccion.get('state')
        )
        return localidad
    
    return "Localidad no encontrada"
