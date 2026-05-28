# generar_dataset.py
import random
import csv
import os
from datetime import datetime, timedelta

random.seed(987654)

def generar_datos_transaccionales(num_registros=100):
    estados_posibles = ['COMPLETADA', 'PENDIENTE', 'FALLIDA', 'CANCELADA', '']
    tiendas = ['Tienda_Norte', 'Tienda_Sur', 'Tienda_Centro', 'Tienda_Este', None]
    
    datos = []
    fecha_base = datetime(2023, 1, 1)
    
    for i in range(1, num_registros + 1):
        tx_id = f"TXN-{str(i).zfill(5)}"
        dias_aleatorios = random.randint(0, 365)
        fecha_tx = fecha_base + timedelta(days=dias_aleatorios)
        
        if random.random() < 0.1:
            fecha_str = fecha_tx.strftime("%d-%m-%Y")
        else:
            fecha_str = fecha_tx.strftime("%Y-%m-%d")
            
        cliente_id = random.randint(1000, 1050) if random.random() > 0.05 else None
        
        monto = round(random.uniform(10.0, 500.0), 2)
        if random.random() < 0.1:
            monto = f"${monto}"
        elif random.random() < 0.05:
            monto = -monto
        elif random.random() < 0.05:
            monto = None
            
        estado = random.choice(estados_posibles)
        tienda = random.choice(tiendas)
        
        registro = {
            'transaction_id': tx_id,
            'date': fecha_str,
            'customer_id': cliente_id,
            'amount': monto,
            'status': estado,
            'store': tienda
        }
        datos.append(registro)
        
        if random.random() < 0.05:
            datos.append(registro.copy())
    
    return datos

# Generar y guardar
datos = generar_datos_transaccionales(100)
os.makedirs('homeworks/data', exist_ok=True)
with open('homeworks/data/transacciones_raw.csv', 'w', newline='', encoding='utf-8') as f:
    campos = ['transaction_id', 'date', 'customer_id', 'amount', 'status', 'store']
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(datos)

print(f"✅ Dataset generado: homeworks/data/transacciones_raw.csv")
print(f"📊 Total registros: {len(datos)}")