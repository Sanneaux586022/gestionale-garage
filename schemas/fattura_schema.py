from marshmallow import Schema, fields


class FatturaResponseSchema(Schema):
    id = fields.Int()
    data_emissione = fields.Date()
    data_scadenza = fields.Date()
    data_pagamento = fields.Date()


class FatturaChiudiSchema(Schema):
    data_pagamento = fields.Date(required=True)


class FatturaConImportoSchema(Schema):
    fattura = fields.Nested(FatturaResponseSchema)
    importo_totale = fields.Decimal()
