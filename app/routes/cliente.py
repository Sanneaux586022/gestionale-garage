from flask import Blueprint, jsonify, request

from database import get_db_session
from models.cliente import Cliente

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/cliente", methods=["POST"])
def add_cliente():

    data = request.get_json()
    db_session = get_db_session()

    try:
        nuovo_cliente = Cliente(
            nome=str(data.get("nome")),
            cognome=str(data.get("cognome")),
            telefono=str(data.get("telefono")),
            email=str(data.get("email")),
        )
        db_session.add(nuovo_cliente)
        db_session.commit()
        return (
            jsonify({"message": f"utente {nuovo_cliente.nome} correttamente generato"}),
            201,
        )

    except Exception as err:
        db_session.rollback()
        print(f"Errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione"}), 500
