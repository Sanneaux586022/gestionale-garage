from marshmallow import Schema, ValidationError, fields, post_load, validates


class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    cognome = fields.Str(
        required=True,
    )
    telefono = fields.Str(required=True)
    email = fields.Email()

    @validates("telefono")
    def valida_telefono(self, value, **kwargs):
        if len(value) < 10 or len(value) > 15:
            raise ValidationError("La lunghezza del numero di telefono non è corretta.")
        if not value.isdigit():
            raise ValidationError("Il numero di telefono deve contenere solo numeri.")

    @post_load
    def normalizza_nominativi(self, data, **kwargs):
        nome = data["nome"]
        cognome = data["cognome"]

        data["nome"] = nome.lower()
        data["cognome"] = cognome.lower()

        return data
