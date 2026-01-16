<div align="center">
  <a href="https://github.com/tu-usuario/phishing-predictor">
    <img src="https://cdn-icons-png.flaticon.com/512/2092/2092663.png" alt="Logo" width="120" height="120">
  </a>

  <h1 align="center">PhishingPredictor™</h1>

  <p align="center">
    <strong>Plataforma de Ciberdefensa Activa basada en Inteligencia Artificial Híbrida</strong>
    <br />
    <em>"Donde la Semántica del LLM encuentra la Precisión del Machine Learning"</em>
  </p>

  <p align="center">
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://flask.palletsprojects.com/">
      <img src="https://img.shields.io/badge/Framework-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    </a>
    <a href="https://www.mongodb.com/">
      <img src="https://img.shields.io/badge/DB-MongoDB_Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
    </a>
    <a href="https://cohere.com/">
      <img src="https://img.shields.io/badge/AI_Core-Cohere_LLM-6d2c9e?style=for-the-badge&logo=openai&logoColor=white" alt="Cohere">
    </a>
    <a href="https://onnx.ai/">
      <img src="https://img.shields.io/badge/Inference-ONNX_Runtime-005CED?style=for-the-badge&logo=onnx&logoColor=white" alt="ONNX">
    </a>
    <br />
    <img src="https://img.shields.io/badge/Maintenance-Active-success?style=flat-square" alt="Maintenance">
    <img src="https://img.shields.io/badge/License-MIT-orange?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/Version-1.0.0_MVP-blue?style=flat-square" alt="Version">
  </p>

  <p align="center">
    <a href="#-introducción">Introducción</a> •
    <a href="#-arquitectura-técnica">Arquitectura</a> •
    <a href="#-características-del-sistema">Características</a> •
    <a href="#-instalación-y-despliegue">Instalación</a> •
    <a href="#-guía-de-uso">Uso</a> •
    <a href="#-roadmap">Roadmap</a> •
    <a href="#-faq">FAQ</a>
  </p>
</div>

<br>

---

## 🚀 Introducción

**PhishingPredictor** representa un cambio de paradigma en la detección de amenazas digitales. Mientras que los antivirus tradicionales se basan en firmas estáticas y "listas negras" (que siempre van un paso por detrás de los atacantes), nuestra solución utiliza un enfoque proactivo y contextual.

El sistema implementa una **Arquitectura Híbrida** revolucionaria que combina dos "cerebros":
1.  **Cerebro Cualitativo (LLM - Cohere):** Capaz de entender el lenguaje natural, la urgencia psicológica y el contexto semántico de un ataque (Ingeniería Social).
2.  **Cerebro Cuantitativo (ML - ONNX):** Capaz de analizar vectores matemáticos de características técnicas (protocolos de red, ofuscación, estructura HTML) con precisión milimétrica.

### 🆚 Comparativa de Enfoques

| Característica | Antivirus Tradicional 🚫 | PhishingPredictor ✅ |
| :--- | :--- | :--- |
| **Detección** | Reactiva (Listas Negras) | Proactiva (Análisis en tiempo real) |
| **Tecnología** | Hashing de URLs | IA Híbrida (NLP + ML) |
| **Ingeniería Social** | Ignora el contexto | Entiende la semántica y psicología |
| **Nuevas Amenazas** | Requiere actualización de BD | Detecta *Zero-Day* attacks |
| **Feedback** | Binario (Bloqueado/Permitido) | Explicativo (Por qué es peligroso) |

---

## 🏛️ Arquitectura Técnica

La robustez de PhishingPredictor reside en su pipeline de procesamiento modular. A continuación se detalla el flujo de datos desde que el usuario introduce una URL hasta que recibe el veredicto.

### 🔄 Diagrama de Flujo (Pipeline)

```mermaid
graph TD
    %% Nodos principales
    User((👤 Usuario))
    WebUI[🖥️ Frontend Web]
    Controller[⚙️ Flask Controller]

    %% Nivel 1
    subgraph "Nivel 1: Procesamiento Semántico (Opcional)"
        Prompt[📝 Prompt Engineering]
        LLM[🤖 Cohere API]
    end

    %% Nivel 2
    subgraph "Nivel 2: Ingeniería de Características"
        Cleaner[🧹 Parser & Sanitización de Datos]
        Vector[🔢 Extracción / Vectorización de Características]
        Fallback[🛡️ Sistema de Reglas / Fallback]
    end

    %% Nivel 3
    subgraph "Nivel 3: Inferencia Matemática (ONNX)"
        Inference[⚡ ONNX Runtime]
        ModelURL[🧮 Modelo URL (RandomForest)]
        ModelText[🧮 Modelo Texto (Transformer)]
    end

    %% Nivel 4
    subgraph "Nivel 4: Persistencia"
        Mongo[(🍃 MongoDB Atlas)]
        GridFS[🗄️ GridFS (Imágenes)]
    end

    %% Flujo
    User -->|Input| WebUI
    WebUI -->|POST Request| Controller

    Controller -->|Texto / URL crudo| Prompt
    Prompt --> LLM
    LLM -->|Salida estructurada| Cleaner

    Cleaner -- Datos válidos --> Vector
    Cleaner -- Datos incompletos --> Fallback

    Vector --> Inference
    Fallback --> Inference

    ModelURL -.-> Inference
    ModelText -.-> Inference

    Inference -->|Probabilidad + Clasificación| Controller
    Controller -->|Persistencia| Mongo
    Controller -->|Respuesta + Explicación| WebUI

### 🧠 Componentes del Núcleo

* **Agente de Extracción (The Detective):** Utiliza el modelo `command-r` de Cohere para analizar la URL y extraer 30 características técnicas basadas en el dataset académico UCI Phishing (ej: `having_IP_Address`, `SSLfinal_State`, `URL_Length`).
* **Motor de Inferencia (The Mathematician):** Los modelos entrenados (`.onnx`) permiten ejecutar predicciones complejas en milisegundos sin depender de librerías pesadas como PyTorch o TensorFlow en producción.
* **Sistema de Resiliencia:** Implementación de bloques `try-except` avanzados y lógica de limpieza de JSON para garantizar que las "alucinaciones" de la IA Generativa no rompan el servicio.

---

## ✨ Características del Sistema

### 1. 🌐 Deep URL Scanner
Análisis profundo de dominios. No solo verificamos si el sitio existe, analizamos:
* **Ofuscación:** Uso de acortadores, `@` en URL, redirecciones dobles (`//`).
* **Infraestructura:** Edad del dominio, validez de certificados SSL/TLS, configuración DNS.
* **Contenido:** Presencia de iframes invisibles o deshabilitación del clic derecho.

### 2. 💬 Smishing & Email Analysis
Protección contra el fraude basado en texto.
* Detecta patrones lingüísticos de **Urgencia** ("Acción inmediata requerida").
* Detecta patrones de **Autoridad** ("Somos la Policía/Hacienda").
* Detecta patrones de **Oferta** ("Has ganado un premio").

### 3. 👁️ Vision Guard (OCR + Análisis)
Módulo capaz de procesar capturas de pantalla.
* Ideal para mensajes de WhatsApp o SMS donde el texto no se puede copiar fácilmente.
* Utiliza modelos multimodales para "ver" la imagen y detectar suplantación de identidad visual.

### 4. 📊 Dashboard Analítico
* **Mapa de Calor:** Visualización geoespacial de los ataques reportados.
* **Estadísticas:** Gráficos de sectores y barras generados dinámicamente con `Matplotlib` y renderizados en Base64 para máxima velocidad.

---

## 📂 Estructura del Proyecto

Una visión detallada de cómo está organizado el código fuente:

```text
phishing-predictor/
├── 📂 static/                   # Assets estáticos (Frontend)
│   ├── 📂 css/                  # Hojas de estilo y temas
│   ├── 📂 js/                   # Scripts del lado del cliente
│   └── 📂 img/                  # Logotipos y recursos gráficos
│
├── 📂 templates/                # Plantillas HTML (Jinja2)
│   ├── home.html                # Página de inicio
│   ├── predictions.html         # Interfaz principal de análisis
│   ├── dashboard.html           # Panel de estadísticas
│   ├── report.html              # Formulario de denuncia
│   ├── minigame.html            # Juego educativo
│   └── presentacion.html        # Slides de defensa del proyecto
│
├── 📂 models/ (Virtual)         # Modelos de IA
│   ├── detector_phishing_uci.onnx  # Modelo URL
│   └── detector_fraude_final.onnx  # Modelo Texto
│
├── .env                         # Variables de entorno (Credenciales)
├── .gitignore                   # Exclusiones de Git
├── app.py                       # 🚀 CORE: Controlador Flask & Lógica
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación
🛠️ Instalación y DesplieguePrerrequisitosPython 3.9 o superior.Cuenta en MongoDB Atlas (Cluster gratuito sirve).API Key de Cohere (Trial key sirve).Paso 1: Clonar RepositorioBashgit clone [https://github.com/TU_USUARIO/phishing-predictor.git](https://github.com/TU_USUARIO/phishing-predictor.git)
cd phishing-predictor
Paso 2: Entorno Virtual (Best Practice)Aislar las librerías es crucial para evitar conflictos.Windows:Bashpython -m venv venv
venv\Scripts\activate
macOS / Linux:Bashpython3 -m venv venv
source venv/bin/activate
Paso 3: Instalar DependenciasBashpip install -r requirements.txt
Paso 4: Configuración de SecretosCrea un archivo llamado .env en la raíz del proyecto y configura tus claves.(Nota: El archivo .env nunca debe subirse al repositorio).Ini, TOML# Database Connection
MONGO_USERNAME=tu_usuario
PASSWORD=tu_contraseña

# AI Services
COHERE_API_KEY=tu_api_key_v2_de_cohere
Paso 5: EjecuciónBashpython app.py
El servidor se iniciará en modo debug. Accede a: http://localhost:5000🗺️ Roadmap (Hoja de Ruta)Nuestro plan de desarrollo para escalar PhishingPredictor de un MVP a un producto SaaS.[x] Q1 2026 - Fase MVP[x] Desarrollo del Core Híbrido (Flask + Cohere + ONNX).[x] Despliegue de Base de Datos MongoDB.[x] Interfaz Web y Dashboard básico.[ ] Q2 2026 - Integración[ ] Plugin Universal: Extensión para navegadores y apps de mensajería (WhatsApp/Telegram).[ ] API Pública: Endpoints REST para uso externo.[ ] Q3 2026 - Mobile & Edge[ ] App Nativa: Escáner de QR maliciosos y protección SMS.[ ] Offline Mode: Optimización de modelos ONNX para correr localmente.[ ] Q4 2026 - MLOps[ ] Real-time Training: Re-entrenamiento automático con nuevos vectores de ataque.❓ FAQ (Preguntas Frecuentes)<details><summary><strong>¿Por qué usar dos IAs en lugar de una?</strong></summary>Usar solo un LLM (como GPT) es lento y caro para analizar millones de URLs. Usar solo Machine Learning clásico pierde el contexto semántico. Al combinarlos, obtenemos la velocidad del ML y la comprensión del LLM.</details><details><summary><strong>¿Se guardan mis datos personales?</strong></summary>No. Solo almacenamos la URL o el texto analizado y el resultado de la predicción de forma anónima para generar estadísticas globales. No guardamos información identificable del usuario.</details><details><summary><strong>¿Qué hago si el sistema marca una web segura como peligrosa?</strong></summary>Ningún sistema es 100% perfecto. Puedes usar la sección "Reportar" para notificar un falso positivo. Nuestro equipo revisará el caso para re-entrenar el modelo.</details>👥 Equipo de DesarrolloProyecto desarrollado con pasión por el equipo CyberShield Team:MiembroRolEspecialidadJavier Hernández💻 Full Stack LeadFlask, Arquitectura WebKareem Barghouti🧠 AI EngineerNLP, Prompt Engineering, CohereAshley Harris📊 Data ScientistModelos ONNX, Pandas, AnalyticsPaco Perelló⚙️ Backend ArchitectMongoDB, API Integration, DevOps📄 LicenciaEste proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.<div align="center"><sub>Desarrollado como Proyecto Educativo Final de Máster/Grado. 2026.</sub><a href="#">⬆ Volver arriba</a></div>