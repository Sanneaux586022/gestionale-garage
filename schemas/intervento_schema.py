from marshmallow import Schema, fields


class InterventoResponseSchema(Schema):
    id = fields.Int()
    id_auto = fields.Int()
    id_meccanico = fields.Int()
    stato_intervento = fields.Str()
    tariffa_oraria_applicata = fields.Decimal()


class InterventoNormaleResponseSchema(InterventoResponseSchema):
    id_preventivo = fields.Int()
