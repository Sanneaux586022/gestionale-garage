from marshmallow import Schema, ValidationError, fields, post_load, validates


class RicambioSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    prezzo_acquisto = fields.Decimal(required=True)
    prezzo_vendita = fields.Decimal(required=True)
    quantita_scorta = fields.Int(required=True)

    @validates("quantita_scorta")
    def valida_quantita_scorta(self, value, **kwargs):
        if value < 0:
            raise ValidationError(
                "La quantita scorta iniziale non puo essere inferiore a 0."
            )

    @post_load
    def normalizza_nome(self, data, **kwargs):
        nome = data["nome"]

        data["nome"] = nome.lower()
        return data


class RicambioQuantitaSchema(Schema):
    quantita = fields.Int(required=True)

    @validates("quantita")
    def valida_qta(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("La quantita non può essere inferiore o uguale a 0.")
