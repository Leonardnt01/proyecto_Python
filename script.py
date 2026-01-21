import pandas as pd 
import matplotlib.pyplot as plt

print("="*60)
print(" ANÁLISIS DE GASTOS PERSONALES")
print("="*60)

#carga los datos del archivo csv

print("\n PASO 2: Cargando datos del CSV...")


archivo = 'gastos_mensual.csv'

try:
    df = pd.read_csv(archivo, sep=';', encoding='latin-1')
    print(f" Datos cargados exitosamente: {len(df)} registros")
except FileNotFoundError:
    print(f" ERROR: No se encontró el archivo '{archivo}'")
    print("   Asegúrate de que el archivo esté en la misma carpeta que este script.")
    exit()



print("\n PASO 3: Primeras filas de tus datos:")
print(df.head())

print("\n Columnas del dataset:")
print(df.columns.tolist())

print("\nℹ Información del dataset:")
print(df.info())

if 'Unnamed: 5' in df.columns:
    df = df.drop('Unnamed: 5', axis=1)
    print(" Columna vacía eliminada")

# 4.2 Limpiar columna Monto (quitar "S/", espacios, convertir coma a punto)

df['Monto'] = df[' Monto '].str.replace('S/', '', regex=False)
df['Monto'] = df['Monto'].str.replace(' ', '', regex=False)
df['Monto'] = df['Monto'].str.replace(',', '.', regex=False)
df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce')
df = df.drop(' Monto ', axis=1)  # esta parte elimina la columna original
print(" Columna 'Monto' convertida a numérico")

# 4.3 Convertir Fecha a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
print(" Columna 'Fecha' convertida a datetime")

df = df.dropna(subset=['Monto'])
print(f" Datos preparados: {len(df)} registros válidos")

#-------------------

print("\n" + "="*60)
print(" VERIFICACIÓN: Datos después de limpieza")
print("="*60)

print("\ Primeras filas LIMPIAS:")
print(df.head())

print("\n2️ Información ACTUALIZADA del dataset:")
print(df.info())

print("\n3️ Verificación de tipos de datos:")
print(f"   • Fecha es tipo: {df['Fecha'].dtype} ✅ (debe ser datetime64)")
print(f"   • Monto es tipo: {df['Monto'].dtype} ✅ (debe ser float64)")

print("\n4️ Muestra de valores en Monto:")
print(f"   Primeros 3 valores: {df['Monto'].head(3).tolist()}")
print(f"   Tipo del primer valor: {type(df['Monto'].iloc[0])}")

print("\n5️ Estadísticas rápidas de Monto (¡ahora sí funciona!):")
print(f"   • Suma total: S/ {df['Monto'].sum():.2f}")
print(f"   • Promedio: S/ {df['Monto'].mean():.2f}")
print(f"   • Máximo: S/ {df['Monto'].max():.2f}")
print(f"   • Mínimo: S/ {df['Monto'].min():.2f}")

print("\ Si ves números arriba (no 'NaN'), ¡los datos están limpios!")

#-------------------
#estadisticas generales

print("\n" + "="*59)
print(" PASO 5: ESTADÍSTICAS GENERALES")
print("="*59)

# Calcular métricas básicas
total_gastado = df['Monto'].sum()
promedio = df['Monto'].mean()
mediana = df['Monto'].median()
minimo = df['Monto'].min()
maximo = df['Monto'].max()

print(f"\n Total gastado:     S/ {total_gastado:,.2f}")
print(f" Promedio:          S/ {promedio:,.2f}")
print(f" Mediana:           S/ {mediana:,.2f}")
print(f" Gasto mínimo:      S/ {minimo:,.2f}")
print(f" Gasto máximo:      S/ {maximo:,.2f}")
print(f" Transacciones:     {len(df)}")

# Calcular promedio diario
dias = (df['Fecha'].max() - df['Fecha'].min()).days + 1
promedio_diario = total_gastado / dias if dias > 0 else 0
print(f" Días analizados:   {dias}")
print(f" Promedio diario:   S/ {promedio_diario:,.2f}")


# PASO 6: ANÁLISIS POR CATEGORÍA

print("\n" + "="*60)
print(" PASO 6: ANÁLISIS POR CATEGORÍA")
print("="*60)

# Agrupar por categoría y calcular estadísticas
por_categoria = df.groupby('Categoría')['Monto'].agg([
    ('Total', 'sum'),
    ('Cantidad', 'count'),
    ('Promedio', 'mean')
]).round(2)

# Ordenar de mayor a menor gasto
por_categoria = por_categoria.sort_values('Total', ascending=False)

# Calcular porcentaje del total
por_categoria['Porcentaje'] = (por_categoria['Total'] / total_gastado * 100).round(2)

print("\n Resumen por categoría:")
print(por_categoria)

print("\n Interpretación:")
categoria_mayor = por_categoria.index[0]
monto_mayor = por_categoria.iloc[0]['Total']
porcentaje_mayor = por_categoria.iloc[0]['Porcentaje']
print(f"   • Tu mayor gasto es en: {categoria_mayor}")
print(f"   • Monto: S/ {monto_mayor:.2f} ({porcentaje_mayor}% del total)")

# ========================================
# PASO 7: TOP 5 GASTOS MÁS ALTOS
# ========================================
print("\n" + "="*60)
print(" PASO 7: TOP 5 GASTOS MÁS ALTOS")
print("="*60)

# Obtener los 5 gastos más grandes
top5 = df.nlargest(5, 'Monto')[['Fecha', 'Categoría', 'Descripción', 'Monto']].copy()

# Formatear la fecha para mejor visualización
top5['Fecha'] = top5['Fecha'].dt.strftime('%d/%m/%Y')

print("\n🏆 Tus 5 gastos más grandes:\n")
for i, row in top5.iterrows():
    print(f"   {row['Fecha']} | {row['Categoría']:15} | {row['Descripción']:30} | S/ {row['Monto']:>6.2f}")

print(f"\n Estos 5 gastos representan S/ {top5['Monto'].sum():.2f} ({top5['Monto'].sum()/total_gastado*100:.1f}% del total)")

# ========================================
# PASO 8: CREAR VISUALIZACIONES
# ========================================
print("\n" + "="*60)
print(" PASO 8: GENERANDO GRÁFICOS...")
print("="*60)

# Configurar el estilo
plt.style.use('seaborn-v0_8-darkgrid')

# Crear figura con 3 gráficos
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(' Análisis Visual de Gastos Personales', fontsize=16, fontweight='bold')

# --- GRÁFICO 1: BARRAS POR CATEGORÍA ---
print("\n Creando gráfico de barras por categoría...")
gastos_cat = df.groupby('Categoría')['Monto'].sum().sort_values(ascending=False)

gastos_cat.plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
axes[0].set_title('Gastos Totales por Categoría', fontweight='bold')
axes[0].set_xlabel('Categoría')
axes[0].set_ylabel('Monto (S/)')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

# Agregar valores encima de las barras
for i, v in enumerate(gastos_cat.values):
    axes[0].text(i, v, f'S/ {v:,.0f}', ha='center', va='bottom', fontsize=9)

# --- GRÁFICO 2: GRÁFICO DE PASTEL ---
print(" Creando gráfico de pastel...")
colores = plt.cm.Set3(range(len(gastos_cat)))

axes[1].pie(gastos_cat.values, 
            labels=gastos_cat.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colores)
axes[1].set_title('Distribución Porcentual por Categoría', fontweight='bold')

# --- GRÁFICO 3: TENDENCIA TEMPORAL ---
print(" Creando gráfico de tendencia temporal...")
gastos_tiempo = df.groupby('Fecha')['Monto'].sum()

gastos_tiempo.plot(kind='line', 
                   ax=axes[2], 
                   marker='o', 
                   color='green',
                   linewidth=2,
                   markersize=6)
axes[2].set_title('Tendencia de Gastos en el Tiempo', fontweight='bold')
axes[2].set_xlabel('Fecha')
axes[2].set_ylabel('Monto (S/)')
axes[2].tick_params(axis='x', rotation=45)
axes[2].grid(True, alpha=0.3)
axes[2].fill_between(gastos_tiempo.index, gastos_tiempo.values, alpha=0.2, color='green')

# Ajustar diseño
plt.tight_layout()

# Guardar gráfico
nombre_imagen = 'analisis_gastos.png'
plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')
print(f"\n Gráficos guardados como '{nombre_imagen}'")

# Mostrar gráficos
print(" Mostrando gráficos en ventana...")
plt.show()

