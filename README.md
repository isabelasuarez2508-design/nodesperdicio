# 🥬 NoDesperdicio

Aplicación web para llevar el control de los alimentos que hay en casa y saber
cuáles vencen pronto, con el fin de reducir el desperdicio de comida.

## Problema que resuelve

Cerca de un tercio de los alimentos que se producen en el mundo se desperdicia.
Gran parte ocurre en los hogares, simplemente porque se nos olvida qué tenemos
y cuándo se vence. **NoDesperdicio** ayuda a verlo de un vistazo.

## Funcionalidades

- Agregar alimentos con nombre, cantidad, categoría y fecha de vencimiento.
- Lista ordenada del que vence primero al que vence después.
- Colores según el estado: en buen estado, vence pronto (3 días o menos) y vencido.
- Resumen con el total, los que vencen pronto, los vencidos y los aprovechados.
- Botón «Lo consumí» para llevar la cuenta de lo aprovechado.
- Página de consejos para no desperdiciar comida.

## Tecnologías

- Python 3
- Flask
- SQLite (incluido en Python)
- HTML5 y CSS3

## Cómo ejecutarlo

```bash
# 1. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python app.py
```

Abre en el navegador: http://127.0.0.1:5000

## Estructura del proyecto

```
nodesperdicio/
├── app.py                 # Rutas y lógica (Flask)
├── requirements.txt
├── templates/
│   ├── base.html          # Plantilla base
│   ├── index.html         # Despensa
│   └── consejos.html      # Consejos
└── static/
    └── css/style.css
```

## Autora

Isabela Suárez López · Estudiante de Análisis y Desarrollo de Software · SENA
