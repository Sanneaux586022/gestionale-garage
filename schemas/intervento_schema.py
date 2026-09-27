from marshmallow import Schema, ValidationError, fields, validates


class InterventoResponseSchema(Schema):
    id = fields.Int()
    id_auto = fields.Int()
    id_meccanico = fields.Int()
    stato_intervento = fields.Str()
    tariffa_oraria_applicata = fields.Decimal()


class InterventoNormaleResponseSchema(InterventoResponseSchema):
    id_preventivo = fields.Int()


class InterventoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_auto = fields.Int(dump_only=True)
    id_meccanico = fields.Int(dump_only=True)
    id_preventivo = fields.Int(dump_only=True)
    id_fattura = fields.Int(dump_only=True)
    stato_intervento = fields.Str(dump_only=True)
    ore_lavorate = fields.Decimal(dump_only=True)
    tariffa_oraria_applicata = fields.Decimal(dump_only=True)
    data_inizio_intervento = fields.Date(dump_only=True)
    data_fine_intervento = fields.Date(dump_only=True)


class InterventoCompletatoSchema(Schema):
    ore_lavorate = fields.Decimal(required=True)

    @validates("ore_lavorate")
    def valida_ore(self, value, **kwargs):
        if value < 0.00:
            raise ValidationError("Il numero di ore lavorate non può essere negativo.")
