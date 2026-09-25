from flask import jsonify


def error_response(message, status_code):
    return jsonify({"errore": message}), status_code

def ok_response(message, status_code=200):
    return jsonify({"response_data": message}), status_code

def validation_error_response():
    return error_response("Dati inseriti non corretti.", 400)


def generic_error_response():
    return error_response("Errore durante l'operazione.", 500)

