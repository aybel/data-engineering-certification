# src/utils/data_loader.py
import pandas as pd
from pathlib import Path

class DataLoader:
    """
    Cargador de datos simple para el proyecto
    Los datasets SIEMPRE están en data/raw/ y data/processed/
    """
    
    def __init__(self):
        # La raíz del proyecto es donde está este archivo (src/utils/)
        # Subimos 2 niveles: src/utils/ -> src/ -> raíz del proyecto
        self.project_root = Path(__file__).parent.parent.parent
        
        # Si no funciona, intentar con el directorio actual
        if not (self.project_root / "data").exists():
            # Buscar hacia arriba hasta encontrar data/
            current = Path.cwd()
            for parent in [current] + list(current.parents):
                if (parent / "data").exists():
                    self.project_root = parent
                    break
        
        # Definir rutas de datos
        self.data_raw = self.project_root / "data" / "raw"
        self.data_processed = self.project_root / "data" / "processed"
        self.data_curated = self.project_root / "data" / "curated"
        
        print(f"📁 Proyecto: {self.project_root}")
        print(f"📁 data/raw: {self.data_raw}")
    
    def list_datasets(self, folder="raw"):
        """Lista todos los datasets en una carpeta"""
        if folder == "raw":
            path = self.data_raw
        elif folder == "processed":
            path = self.data_processed
        elif folder == "curated":
            path = self.data_curated
        else:
            raise ValueError("folder must be 'raw', 'processed', or 'curated'")
        
        if not path.exists():
            print(f"❌ {folder}/ no existe")
            return []
        
        files = list(path.glob("*.csv")) + list(path.glob("*.xlsx"))
        if files:
            print(f"\n📊 Datasets en {folder}/:")
            for f in files:
                size = f.stat().st_size / (1024*1024)
                print(f"  - {f.name} ({size:.2f} MB)")
        else:
            print(f"📁 No hay datasets en {folder}/")
        
        return files
    
    def load_csv(self, filename, folder="raw", **kwargs):
        """Carga un archivo CSV desde data/folder/"""
        if folder == "raw":
            path = self.data_raw
        elif folder == "processed":
            path = self.data_processed
        elif folder == "curated":
            path = self.data_curated
        else:
            raise ValueError("folder must be 'raw', 'processed', or 'curated'")
        
        file_path = path / filename
        
        if file_path.exists():
            print(f"✅ Cargando: {file_path}")
            df = pd.read_csv(file_path, **kwargs)
            print(f"📊 Shape: {df.shape}")
            return df
        else:
            print(f"❌ Archivo no encontrado: {file_path}")
            print(f"   Asegúrate de que el archivo esté en {path}/")
            return None
    
    def save_csv(self, df, filename, folder="processed", **kwargs):
        """Guarda un DataFrame en data/folder/"""
        if folder == "raw":
            path = self.data_raw
        elif folder == "processed":
            path = self.data_processed
        elif folder == "curated":
            path = self.data_curated
        else:
            raise ValueError("folder must be 'raw', 'processed', or 'curated'")
        
        # Crear directorio si no existe
        path.mkdir(parents=True, exist_ok=True)
        
        file_path = path / filename
        df.to_csv(file_path, index=False, **kwargs)
        print(f"✅ Guardado en: {file_path}")
        return file_path

# Crear una instancia global
loader = DataLoader()