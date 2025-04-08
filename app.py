from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/', methods=['GET'])
def root():
    return "Hello World"

@app.route('/test-connection', methods=['GET'])
def test_connection():
    try:
        # Print connection details (don't expose the key in production)
        print(f"URL: {url}")
        print(f"Key exists: {bool(key)}")
        
        # Test a simple query
        response = supabase.table('peliculas').select('count').execute()
        return jsonify({"connection": "success", "response": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/peliculas', methods=['GET'])
def get_peliculas():
    try:
        response = supabase.table('peliculas').select('*').execute() # query de postgres a nuestra db
        return jsonify({"peliculas": response.data}), 200 
    except Exception as e:
        return jsonify({"error": str(e)}) , 500
        

@app.route("/peliculas", methods= ["POST"])
def agregar_pelicula():
    data = request.get_json()

    # Validación básica
    nombre = data.get('nombre')
    duracion = data.get('duracion')
    director = data.get('director')
    releaseYear = data.get('releaseYear')

    if not all([nombre, duracion, director, isinstance(releaseYear, int)]):
        return jsonify({'error': 'Datos inválidos'}), 400

    nueva_pelicula = {
        'nombre': nombre,
        'duracion': duracion,
        'director': director,
        'releaseYear': releaseYear
    }
    
    response = supabase.table("peliculas").insert(nueva_pelicula).execute()

    # Aquí podrías guardar la película en una base de datos
    return jsonify({'mensaje': 'Película agregada', 'pelicula': nueva_pelicula}), 201



if __name__ == '__main__':
    app.run(debug=True)