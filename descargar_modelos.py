#!/usr/bin/env python3
"""
Descargar modelos necesarios para faceid_engine
"""
import os
import urllib.request
import zipfile

def descargar_modelo():
    """Descarga el modelo de landmarks de dlib si no existe"""
    
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    modelo_path = os.path.join(models_dir, 'shape_predictor_68_face_landmarks.dat')
    
    if os.path.exists(modelo_path):
        print(f"✓ Modelo ya existe: {modelo_path}")
        return True
    
    print("📥 Descargando modelo de landmarks...")
    
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    temp_file = os.path.join(models_dir, 'shape_predictor_68_face_landmarks.dat.bz2')
    
    try:
        # Descargar
        urllib.request.urlretrieve(url, temp_file)
        print(f"✓ Descargado: {temp_file}")
        
        # Descomprimir
        import bz2
        with bz2.BZ2File(temp_file) as f_in:
            with open(modelo_path, 'wb') as f_out:
                f_out.writelines(f_in)
        
        os.remove(temp_file)
        print(f"✓ Modelo extraído: {modelo_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error descargando modelo: {e}")
        return False

if __name__ == "__main__":
    if descargar_modelo():
        print("\n✅ Modelo listo para usar")
    else:
        print("\n❌ No se pudo descargar el modelo")
        exit(1)
