## Proyecto Final - Sistemas de Adquisición y Distribución de Datos

Este proyecto permite leer datos desde un puerto serial, procesarlos, almacenarlos en una base de datos SQLite y enviar notificaciones por correo electrónico usando SMTP. 

### Requisitos Previos

1. **Python 3.9 o superior**: Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/).
2. **SQLite**: Se utiliza como base de datos local.
3. **Puerto Serial**: Configurado para recibir datos con el formato `valor;0 o 1`.
4. **Credenciales SMTP**: Para enviar correos electrónicos.

---

### Configuración del Proyecto

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/Dariusss12/proyecto_final_scada
cd proyecto_final_scada
```

#### 2. Crear un Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido, reemplazando los valores con tus credenciales:

```env
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password
EMAIL_RECIPIENT=recipient@example.com

SERIAL_PORT="your_serial_port"
```

Ajusta la variable `SERIAL_PORT` según tu sistema operativo y el puerto a utilizar:

- **Windows**: `"COM3"`
- **Linux**: `"/dev/ttyUSB0"`

---

### Ejecución del Proyecto

1. Asegúrate de que tu dispositivo serial esté enviando datos con el formato `valor_numerico;booleano(0 o 1)`.
2. Inicia el servidor con el siguiente comando:

```bash
uvicorn main:app --reload
```

3. El servidor estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000).

