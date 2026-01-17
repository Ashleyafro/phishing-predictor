import sys
import os
import numpy as np

# Spark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col, when

# Scikit-Learn & ONNX
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.pipeline import Pipeline as SklearnPipeline
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt

# Corrección Windows
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# ---------------------------------------------------------
# 1. CARGAR DATOS
# ---------------------------------------------------------
print("🚀 Iniciando Spark con Dataset UCI...")
spark = SparkSession.builder \
    .appName("DetectorPhishingAvanzado") \
    .master("local[*]") \
    .getOrCreate()

# Ruta inteligente (busca en la misma carpeta del script)
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(carpeta_actual, "dataset_phishing.csv")

if not os.path.exists(ruta_csv):
    print(f"❌ ERROR: No encuentro {ruta_csv}")
    sys.exit(1)

df = spark.read.csv(ruta_csv, header=True, inferSchema=True)

# ---------------------------------------------------------
# 2. PREPARACIÓN DE DATOS
# ---------------------------------------------------------
# Convertir -1 a 1 (Fraude) y el resto a 0
data = df.withColumn("label", when(col("Result") == -1, 1).otherwise(0))

# MEJORA: Excluir 'index' (no aporta valor) y las etiquetas
columnas_input = [c for c in df.columns if c not in ["Result", "label", "index"]]
print(f"✅ Variables seleccionadas ({len(columnas_input)}): {columnas_input[:5]}...")

assembler = VectorAssembler(inputCols=columnas_input, outputCol="features")
(trainingData, testData) = data.randomSplit([0.8, 0.2], seed=1234)

# ---------------------------------------------------------
# 3. ENTRENAMIENTO
# ---------------------------------------------------------
print("🧠 Entrenando modelo matemático...")
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=20, regParam=0.01, family="binomial")
pipeline = Pipeline(stages=[assembler, lr])
model = pipeline.fit(trainingData)

# Evaluación
preds = model.transform(testData)
evaluator = BinaryClassificationEvaluator(labelCol="label")
print(f"✅ Precisión (AUC) del modelo: {evaluator.evaluate(preds):.2%}")

# ---------------------------------------------------------
# 4. EXPORTACIÓN A ONNX (CORREGIDA)
# ---------------------------------------------------------
print("\n🏗️ Exportando a ONNX...")

# Extraer pesos de Spark
lr_model = model.stages[1]
coeficientes = lr_model.coefficientMatrix.toArray() 
intercepto = lr_model.interceptVector.toArray()

# Crear modelo espejo
dummy_lr = SklearnLogisticRegression()

# --- CORRECCIÓN AQUÍ ---
# Inicializamos con 2 filas (una para clase 0, otra para clase 1)
# para que Scikit-Learn no se queje de "solo una clase".
X_dummy = np.zeros((2, len(columnas_input)))
y_dummy = [0, 1] 
dummy_lr.fit(X_dummy, y_dummy) 
# -----------------------

# Inyectar Pesos reales
dummy_lr.classes_ = np.array([0, 1])
dummy_lr.coef_ = coeficientes
dummy_lr.intercept_ = intercepto

# Guardar ONNX
initial_type = [('input_features', FloatTensorType([None, len(columnas_input)]))]
nombre_archivo = "detector_phishing_uci.onnx"

onnx_model = convert_sklearn(dummy_lr, initial_types=initial_type)
with open(nombre_archivo, "wb") as f:
    f.write(onnx_model.SerializeToString())

print(f"🎉 Modelo guardado: {os.path.abspath(nombre_archivo)}")

# ---------------------------------------------------------
# 5. PRUEBA DE FUEGO
# ---------------------------------------------------------
print("\n--- TEST ONNX ---")
sess = rt.InferenceSession(nombre_archivo)
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

# Simulamos características de una web (30 variables)
# Caso de prueba: Una web con características negativas (-1 en el dataset suele ser malo)
datos_prueba = np.full((1, len(columnas_input)), -1, dtype=np.float32)

pred = sess.run([label_name], {input_name: datos_prueba})[0]
print(f"Web con valores sospechosos (-1): {'FRAUDE 🚨' if pred[0] == 1 else 'SEGURA ✅'}")