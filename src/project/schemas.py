from project import ma
from project.models import Usuario, Empresa


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        load_only = ('password', )


class EmpresaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa


usuario_schema = UsuarioSchema()
empresa_schema = EmpresaSchema()
