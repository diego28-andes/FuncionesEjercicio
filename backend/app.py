from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from controladores import (
    RecetasController,
    IngredientesController,
    )

app = Flask(__name__)
app.config["SECRET_KEY"] = "cookhub-secret-key"
CORS(app)

api = Api(app)

# Rutas para recetas
api.add_resource(RecetasController, "/api/recetas")
#api.add_resource(VistaReceta, "/api/recetas/<int:id_receta>")

# Rutas para ingredientes
api.add_resource(IngredientesController, "/api/ingredientes")
#api.add_resource(VistaIngrediente, "/api/ingredientes/<int:id_ingrediente>")

# Ruta para reportes
#api.add_resource(VistaReporteIngredientes, "/api/reportes/ingredientes")

if __name__ == "__main__":
    print("👨‍🍳 CookHub Backend iniciado en http://localhost:5001")
    print("📊 Endpoints disponibles:")
    print("   GET/POST /api/recetas")
    print("   GET/PUT/DELETE /api/recetas/<id>")
    print("   GET/POST /api/ingredientes")
    print("   GET/PUT/DELETE /api/ingredientes/<id>")
    print("   GET /api/reportes/ingredientes")
    app.run(debug=True, port=5001)
