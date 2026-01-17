import sys
import os
import numpy as np

# Librerías Spark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, CountVectorizer, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col

# Librerías para el "Puente" y Exportación
from sklearn.feature_extraction.text import CountVectorizer as SklearnCountVectorizer
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.pipeline import Pipeline as SklearnPipeline
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
import onnxruntime as rt

# --- CORRECCIÓN WINDOWS ---
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# ---------------------------------------------------------
# 1. ENTRENAMIENTO EN SPARK
# ---------------------------------------------------------
print("🚀 Iniciando Spark...")
spark = SparkSession.builder \
    .appName("DetectorFraudeSMS") \
    .master("local[*]") \
    .getOrCreate()

# Cargar y Limpiar
df = spark.read.csv("spam.csv", header=True, inferSchema=True, encoding='ISO-8859-1')
data = df.select(col("v1").alias("etiqueta_texto"), col("v2").alias("mensaje")).dropna()
data = data.filter(col("etiqueta_texto").isin(["ham", "spam"])) # Filtro anti-errores

(trainingData, testData) = data.randomSplit([0.8, 0.2], seed=1234)

print("🧠 Entrenando modelo en Spark...")

indexer = StringIndexer(inputCol="etiqueta_texto", outputCol="label")
tokenizer = Tokenizer(inputCol="mensaje", outputCol="words")
cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=3000) 
lr = LogisticRegression(maxIter=10, regParam=0.001, family="binomial")

spark_pipeline = Pipeline(stages=[indexer, tokenizer, cv, lr])
spark_model = spark_pipeline.fit(trainingData)

# Evaluación
preds = spark_model.transform(testData)
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print(f"✅ Precisión del modelo Spark: {evaluator.evaluate(preds):.2%}")

# ---------------------------------------------------------
# 2. EXTRACCIÓN DE DATOS DE SPARK
# ---------------------------------------------------------
print("\n🏗️ Preparando inyección de datos...")

# A. Vocabulario
vocabulario_spark = spark_model.stages[2].vocabulary

# B. Pesos (Matriz)
coeficientes_spark = spark_model.stages[3].coefficientMatrix.toArray()
intercepto_spark = spark_model.stages[3].interceptVector.toArray()

# ---------------------------------------------------------
# 3. RECONSTRUCCIÓN EN SCIKIT-LEARN (VERSIÓN CORREGIDA)
# ---------------------------------------------------------
# Pasamos el vocabulario directamente al constructor.
# Esto hace que Scikit se configure internamente mucho mejor.
dummy_cv = SklearnCountVectorizer(vocabulary=vocabulario_spark)
dummy_lr = SklearnLogisticRegression()

sklearn_pipeline = SklearnPipeline([
    ('vect', dummy_cv),
    ('clf', dummy_lr)
])

# INYECCIÓN
# Hacemos un fit con datos falsos para inicializar estructuras
dummy_cv.fit(["test"])

# CORRECCIÓN DEL ERROR 'NoneType' and 'set':
# En lugar de None, usamos set() (conjunto vacío)
dummy_cv.stop_words_ = set() 

# Inyectamos pesos
dummy_lr.classes_ = np.array([0, 1])
dummy_lr.coef_ = coeficientes_spark 
dummy_lr.intercept_ = intercepto_spark

print("💾 Guardando ONNX...")

initial_type = [('input_text', StringTensorType([None, 1]))]

try:
    onnx_model = convert_sklearn(sklearn_pipeline, initial_types=initial_type)
    
    nombre_archivo = "detector_fraude_final.onnx"
    with open(nombre_archivo, "wb") as f:
        f.write(onnx_model.SerializeToString())

    print(f"🎉 ¡ÉXITO TOTAL! Modelo guardado en: {os.path.abspath(nombre_archivo)}")

    # ---------------------------------------------------------
    # 4. PRUEBA FINAL
    # ---------------------------------------------------------
    print("\n--- VERIFICACIÓN DEL ARCHIVO ONNX GENERADO ---")
    sess = rt.InferenceSession(nombre_archivo)
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    
    # Prueba 1: Fraude
    frase1 = np.array([["URGENT! You have won a 1000 prize"]]).reshape(-1, 1)
    pred1 = sess.run([label_name], {input_name: frase1})[0]
    
    # Prueba 2: Normal
    frase2 = np.array([["Hey man, are we meeting later?"]]).reshape(-1, 1)
    pred2 = sess.run([label_name], {input_name: frase2})[0]
    
    print(f"Frase: 'You have won a prize' -> {'FRAUDE 🚨' if pred1[0] == 1 else 'LEGÍTIMO ✅'}")
    print(f"Frase: 'Hey man'              -> {'FRAUDE 🚨' if pred2[0] == 1 else 'LEGÍTIMO ✅'}")

except Exception as e:
    print(f"❌ Error final: {e}")