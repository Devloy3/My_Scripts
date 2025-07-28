from tinydb import TinyDB


db = TinyDB('./datos/datos_personales.json')
trabajo = db.table('trabajo')
sonido = db.table('Sonido')
mar = db.table('Mar')
