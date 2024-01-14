
def obtener_ultimo_id(coleccion):
    # Obtener el último documento ordenando por el campo _id de forma descendente
    ultimo_documento = coleccion.find_one({}, sort=[("_id", -1)])

    # Obtener el último id o establecer a 0 si la colección está vacía
    ultimo_id = ultimo_documento["_id"] + 1 if ultimo_documento else 0

    return ultimo_id
