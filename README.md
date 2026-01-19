# 💹 Sistema Agente Financiero

Sistema de automatización financiera inteligente que combina análisis predictivo en Python con orquestación de flujos mediante n8n. Monitorea mercados en tiempo real, toma decisiones autónomas y ejecuta operaciones financieras automatizadas.

## 🧠 Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| **Python** | Lógica de negocio y análisis de datos |
| **n8n** | Orquestación de flujos de trabajo automatizados |
| **Pandas & NumPy** | Procesamiento de datos financieros |
| **scikit-learn** | Modelos predictivos y análisis ML |
| **Requests & APIs REST** | Conexión con servicios financieros |
| **SQLite/PostgreSQL** | Almacenamiento de datos y transacciones |
| **Streamlit** (opcional) | Dashboard de monitoreo |

## 🖥️ Requisitos del Sistema

### Entorno de Desarrollo Probado
- **Dispositivo:** ASUS TUF GAMING A15
- **Procesador:** AMD Ryzen 7 5800H (8 núcleos, 16 hilos, 3.2 GHz base / 4.4 GHz turbo)
- **Tarjeta gráfica:** NVIDIA GeForce RTX 3060 (6GB GDDR6) - *Opcional para ML avanzado*
- **RAM:** 16 GB DDR4 (3200 MHz)
- **Sistema Operativo:** Windows 11 Pro 64-bit / Ubuntu 22.04 LTS
- **Almacenamiento:** SSD NVMe 1TB (3500 MB/s lectura, 3000 MB/s escritura)
- **Red:** Conexión estable a internet (50+ Mbps)

### Especificaciones Mínimas
- **CPU:** 4 núcleos
- **RAM:** 8 GB
- **Almacenamiento:** SSD 256 GB
- **Conexión:** 10 Mbps estable
- **Python:** 3.9+

### Especificaciones Recomendadas (Producción)
- **CPU:** 8+ núcleos
- **RAM:** 16+ GB
- **Conexión:** Red redundante, servidor 24/7

## 📁 Estructura del Proyecto
agente-financiero/
├── pycache/ # Caché de Python
├── assets/ # Recursos gráficos (iconos, logos)
├── utils/ # Utilidades y funciones auxiliares
├── app.py # Aplicación principal
├── config.py # Configuración del sistema
├── finanzas.json # Datos financieros y configuraciones
├── requirements.txt # Dependencias de Python
├── wf2.json # Flujos de trabajo n8n (exportación 1)
├── workflow.json # Flujos de trabajo n8n (exportación 2)
└── README.md # Documentación del proyecto
