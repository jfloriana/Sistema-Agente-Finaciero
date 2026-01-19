💹 SISTEMA AGENTE FINANCIERO
Sistema de automatización financiera inteligente que combina análisis predictivo en Python con orquestación de flujos mediante n8n. Monitorea mercados en tiempo real, toma decisiones autónomas y ejecuta operaciones financieras automatizadas.

🧠 Tecnologías utilizadas
Python – Lógica de negocio y análisis de datos
n8n – Orquestación de flujos de trabajo automatizados
Pandas & NumPy – Procesamiento de datos financieros
scikit-learn – Modelos predictivos y análisis ML
Requests & APIs REST – Conexión con servicios financieros
SQLite/PostgreSQL – Almacenamiento de datos y transacciones
Streamlit (opcional) – Dashboard de monitoreo

🖥️ Requisitos del sistema (entorno de desarrollo)
Este sistema fue desarrollado y probado en el siguiente entorno:

Dispositivo: ASUS TUF GAMING A15
Procesador: AMD Ryzen 7 5800H (8 núcleos, 16 hilos, 3.2 GHz base / 4.4 GHz turbo)
Tarjeta gráfica: NVIDIA GeForce RTX 3060 (6GB GDDR6) - Opcional para ML avanzado
RAM instalada: 16 GB DDR4 (3200 MHz) - (15.4 GB utilizable)
Sistema operativo: Windows 11 Pro - 64 bits / Ubuntu 22.04 LTS
Almacenamiento: SSD NVMe 1TB (lectura: 3500 MB/s, escritura: 3000 MB/s)
Red: Conexión estable a internet (50+ Mbps recomendado)

⚠️ Mínimo requerido: 4 núcleos CPU, 8 GB RAM, SSD, conexión estable 10 Mbps, Python 3.9+
⚠️ Para producción: 8+ núcleos, 16+ GB RAM, conexión redundante, servidor 24/7

📁 Estructura del proyecto
agente-financiero/
├── __pycache__/           # Caché de Python
├── assets/                # Recursos gráficos, iconos, logos
├── utils/                 # Utilidades y funciones auxiliares
├── app.py                 # Aplicación principal Flask/Streamlit
├── config.py              # Configuración del sistema
├── finanzas.json          # Datos financieros y configuraciones
├── requirements.txt       # Dependencias de Python
├── wf2.json              # Flujos de trabajo n8n (exportación 1)
├── workflow.json          # Flujos de trabajo n8n (exportación 2)
└── README.md              # Documentación del proyecto
