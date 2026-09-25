from marshmallow import Schema, fields


class PreventivoSchema(Schema):
    id = fields.Int(dump_only=True)
    descrizione_lavoro = fields.Str(required=True)
    importo_stimato = fields.Decimal(required=True)
    data_preventivo = fields.Date(dump_only=True)
