# Cromovital | Inventario de pulseras naturales

Proyecto didáctico en Python para practicar clases abstractas, interfaces mediante `Protocol`, herencia y polimorfismo con un inventario de pulseras de piedras naturales.

## Funciones

- Registra modelos de pulsera de amatista, cuarzo rosa u obsidiana con SKU, precio y stock inicial.
- Registra entradas o reposiciones y ventas; una venta descuenta existencias únicamente cuando hay suficiente stock.
- Consulta inventario valorizado e historial de movimientos con fecha, cantidad e importe.
- Guarda los datos en `datos_cromovital.json` junto al programa y los recupera al volver a abrirlo. El primer inicio carga productos de ejemplo; reemplaza o elimina el archivo de datos si quieres iniciar un catálogo vacío.

Para abrir el menú, ejecuta `python inventario.py`. Los importes se manejan en pesos mexicanos. El JSON local es apropiado para una demostración en una computadora; para uso simultáneo por varios empleados se recomienda una base de datos compartida.

Para correr las pruebas automatizadas: `python -m unittest -v`.

## Presentación oral

El archivo [Presentacion_Cromovital_3a5min.pptx](presentacion/Presentacion_Cromovital_3a5min.pptx) contiene nueve diapositivas, notas del presentador para una exposición de aproximadamente cuatro minutos, espacios para capturas de la demostración y las pruebas, y una diapositiva para insertar el video final.
