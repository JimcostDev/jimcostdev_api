# convertir _id en id de una lista de documentos
def convert_object_id_to_str_multi(documents: list, model):
    """
    Convierte el campo '_id' en 'id' como string en una lista de documentos y los 
    convierte en instancias del modelo Pydantic que se le pase.

    :param documents: Lista de documentos devueltos por MongoDB
    :param model: Modelo Pydantic al cual mapear los documentos
    :return: Lista de instancias del modelo Pydantic
    """
    return [model(**doc, id=str(doc['_id'])) for doc in documents if '_id' in doc]


# convertir _id en id de un solo documento
def convert_object_id_to_str_single(doc, model):
    """
    Convierte el campo '_id' en 'id' como string en un documento y lo convierte en una 
    instancia del modelo Pydantic que se le pase.

    :param doc: Documento devuelto por MongoDB
    :param model: Modelo Pydantic al cual mapear el documento
    :return: Instancia del modelo Pydantic
    """
    return model(**doc, id=str(doc['_id'])) if '_id' in doc else None