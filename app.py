from flask import Flask, jsonify, request

# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS  # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app)  # modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/aventur"
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # none
db = SQLAlchemy(app)  # crea el objeto db de la clase SQLAlquemy
ma = Marshmallow(app)  # crea el objeto ma de de la clase Marshmallow


# defino las tablas
class Paquete(db.Model):  # la clase paquete hereda de db.Model
    id = db.Column(db.Integer, primary_key=True)  # define los campos de la tabla
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(2000))
    fecha_salida = db.Column(db.Date, nullable=False)
    fecha_regreso = db.Column(db.Date, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    noches = db.Column(db.Integer, nullable=False)
    lugar_partida = db.Column(db.String(50), nullable=False, default="Buenos Aires")
    destinos = db.Column(db.String(200), nullable=False)
    excursiones = db.Column(db.Integer, default=0)
    seguro = db.Column(db.Boolean, default=True)
    traslado = db.Column(db.Boolean, default=True)
    alquiler_auto = db.Column(db.Boolean, default=True)
    precio_actual = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)
    imagen = db.Column(db.String(400))

    def __init__(
        self,
        titulo,
        descripcion,
        fecha_salida,
        fecha_regreso,
        dias,
        noches,
        lugar_partida,
        destinos,
        excursiones,
        seguro,
        traslado,
        alquiler_auto,
        precio_actual,
        stock,
        imagen,
    ):  # crea el  constructor de la clase
        self.titulo = titulo  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.descripcion = descripcion
        self.fecha_salida = fecha_salida
        self.fecha_regreso = fecha_regreso
        self.dias = dias
        self.noches = noches
        self.lugar_partida = lugar_partida
        self.destinos = destinos
        self.excursiones = excursiones
        self.seguro = seguro
        self.traslado = traslado
        self.alquiler_auto = alquiler_auto
        self.precio_actual = precio_actual
        self.stock = stock
        self.imagen = imagen

    #  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas


#  ************************************************************
class PaqueteSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "titulo",
            "descripcion",
            "fecha_salida",
            "fecha_regreso",
            "dias",
            "noches",
            "lugar_partida",
            "destinos",
            "excursiones",
            "seguro",
            "traslado",
            "alquiler_auto",
            "precio_actual",
            "stock",
            "imagen",
        )


paquete_schema = PaqueteSchema()  # El objeto paquete_schema es para traer un paquete
paquetes_schema = PaqueteSchema(
    many=True
)  # El objeto paquetes_schema es para traer multiples registros de paquete


# crea los endpoint o rutas (json)
@app.route("/paquetes", methods=["GET"])
def get_paquetes():
    all_paquetes = Paquete.query.all()  # el metodo query.all() lo hereda de db.Model
    result = paquetes_schema.dump(
        all_paquetes
    )  # el metodo dump() lo hereda de ma.schema y
    # trae todos los registros de la tabla
    return jsonify(result)  # retorna un JSON de todos los registros de la tabla


@app.route("/paquetes/<id>", methods=["GET"])
def get_paquete(id):
    paquete = Paquete.query.get(id)
    return paquete_schema.jsonify(
        paquete
    )  # retorna el JSON de un paquete recibido como parametro


@app.route("/paquetes/<id>", methods=["DELETE"])
def delete_paquete(id):
    paquete = Paquete.query.get(id)
    db.session.delete(paquete)
    db.session.commit()  # confirma el delete
    return paquete_schema.jsonify(
        paquete
    )  # me devuelve un json con el registro eliminado


@app.route("/paquetes", methods=["POST"])  # crea ruta o endpoint
def create_paquete():
    # print(request.json)  # request.json contiene el json que envio el cliente

    titulo = request.json["titulo"]
    descripcion = request.json["descripcion"]
    fecha_salida = request.json["fecha_salida"]
    fecha_regreso = request.json["fecha_regreso"]
    dias = request.json["dias"]
    noches = request.json["noches"]
    lugar_partida = request.json["lugar_partida"]
    destinos = request.json["destinos"]
    excursiones = request.json["excursiones"]
    seguro = request.json["seguro"]
    traslado = request.json["traslado"]
    alquiler_auto = request.json["alquiler_auto"]
    precio_actual = request.json["precio_actual"]
    stock = request.json["stock"]
    imagen = request.json["imagen"]

    new_paquete = Paquete(
        titulo,
        descripcion,
        fecha_salida,
        fecha_regreso,
        dias,
        noches,
        lugar_partida,
        destinos,
        excursiones,
        seguro,
        traslado,
        alquiler_auto,
        precio_actual,
        stock,
        imagen,
    )

    db.session.add(new_paquete)
    db.session.commit()  # confirma el alta
    return paquete_schema.jsonify(new_paquete)


@app.route("/paquetes/<id>", methods=["PUT"])
def update_paquete(id):
    paquete = Paquete.query.get(id)

    paquete.titulo = request.json["titulo"]
    paquete.descripcion = request.json["descripcion"]
    paquete.fecha_salida = request.json["fecha_salida"]
    paquete.fecha_regreso = request.json["fecha_regreso"]
    paquete.dias = request.json["dias"]
    paquete.noches = request.json["noches"]
    paquete.lugar_partida = request.json["lugar_partida"]
    paquete.destinos = request.json["destinos"]
    paquete.excursiones = request.json["excursiones"]
    paquete.seguro = request.json["seguro"]
    paquete.traslado = request.json["traslado"]
    paquete.alquiler_auto = request.json["alquiler_auto"]
    paquete.precio_actual = request.json["precio_actual"]
    paquete.stock = request.json["stock"]
    paquete.imagen = request.json["imagen"]

    db.session.commit()  # confirma el cambio
    return paquete_schema.jsonify(paquete)  # y retorna un json con el paquete


# programa principal *******************************
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # ejecuta el servidor Flask en el puerto 5000
