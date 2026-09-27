from marshmallow import Schema, ValidationError, fields, validates


class InterventoRicambioSchema(Schema):
    id = fields.Int(dump_only=True)
    quantita_usata = fields.Int(required=True)
    fatturabile = fields.Bool(load_default=True)

    @validates("quantita_usata")
    def valida_qta_usata(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("La quantita usata deve essere positiva")


class InterventoRicambioResponseSchema(Schema):
    id = fields.Int()
    id_intervento = fields.Int()
    id_ricambio = fields.Int()
    quantita_usata = fields.Int()
    prezzo_applicato = fields.Decimal()
    fatturabile = fields.Bool()
