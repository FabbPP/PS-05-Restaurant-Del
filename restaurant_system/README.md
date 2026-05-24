# Sistema Restaurante + Delivery

Arquitectura modular con Django, SQLite y validaciones defensivas. Diseñado con enfoque QA (PE/AVL), robustez ante entradas maliciosas y separación clara de responsabilidades.

## Arquitectura
- **Presentación:** Views + Forms (validación de entrada).
- **Aplicación:** Services (reglas de negocio, transacciones).
- **Dominio:** Models + validaciones + restricciones DB.
- **Infraestructura:** logging y middleware básico.

## Módulos (Django apps)
- **core:** base models, enums, validadores, middleware.
- **users:** autenticación y roles.
- **customers:** clientes y direcciones.
- **catalog:** categorías y productos.
- **inventory:** stock y movimientos.
- **dining:** mesas y estados.
- **orders:** órdenes e ítems.
- **delivery:** delivery, cobertura y repartidores.
- **kitchen:** tickets de cocina.
- **payments:** pagos.
- **billing:** facturación.

## Instalación
```bash
python -m pip install -r requirements/base.txt
```

## Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## Ejecutar servidor
```bash
python manage.py runserver
```

## Estructura del proyecto
```
restaurant_system/
├── apps/
├── tests/
├── docs/
├── requirements/
├── README.md
├── manage.py
```

## Validaciones y restricciones (resumen)
- **Campos obligatorios:** nombre, dirección delivery, número de mesa.
- **Numéricos:** stock >= 0, precio > 0, total >= 0, cantidad > 0.
- **Formato:** email válido, teléfono E.164 o 9-15 dígitos.
- **Estados:** enums cerrados y transiciones en services.

## PE (Partición de Equivalencia)
Ejemplo `Producto.precio`:
- **Válido:** `0.01..9999.99`
- **Inválido:** `<= 0` o `> 10000`

## AVL (Análisis de Valores Límite)
Ejemplo `DetalleOrden.cantidad`:
- 0 → **inválido**
- 1 → **válido**
- 100 → **válido**
- 101 → **inválido**

## Casos de prueba esperados (ejemplos)
- **Válido:** crear orden con items y stock suficiente.
- **Inválido:** cantidad negativa o cero.
- **Límite:** stock = 0 (válido, pero no permite agregar items).
- **Malicioso:** strings muy largos o con caracteres especiales.

## Manejo de errores
Validaciones se aplican en:
1. **Forms**
2. **Models (`clean` + constraints)**
3. **Services**

Las reglas críticas usan transacciones y bloqueos (`select_for_update`) en stock.

## Flujo general
1. Crear orden (mesa o delivery).
2. Añadir items con validación de stock.
3. Ticket de cocina y cambios de estado.
4. Pago y facturación.

## Rutas básicas (JSON)
Ejemplos:
- `GET /health/`
- `POST /catalog/categories/create/`
- `POST /orders/create/`
- `POST /orders/items/create/`
- `POST /delivery/create/`
- `POST /payments/create/`

> Todas las rutas usan formularios Django para validación.
