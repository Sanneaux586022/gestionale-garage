from marshmallow import Schema, ValidationError, fields, pre_load, validate


class AutoSchema(Schema):
    id = fields.Int(dump_only=True)
    targa = fields.Str(
        required=True, validate=validate.Regexp(r"^[A-Z]{2}[0-9]{3}[A-Z]{2}$")
    )
    modello = fields.Str(required=True)
    anno = fields.Int(required=True)

    @pre_load
    def normalizza_targa(self, data, **kwargs):

        targa_upper = data.get("targa")
        if not targa_upper:
            raise ValidationError("Nessuna targa inviata.")

        data["targa"] = targa_upper.upper()
        return data
