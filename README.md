# Cromovital | Inventario de pulseras naturales

Proyecto didáctico en Python para practicar clases abstractas, interfaces mediante `Protocol`, herencia y polimorfismo con un inventario de pulseras de piedras naturales.

## Requisitos

- Python 3.10 o posterior
- Visual Studio Code
- Extensión oficial **Python** de Microsoft en VS Code (recomendable)

## Abrir en Visual Studio Code

1. Descomprime o conserva esta carpeta en una ubicación de trabajo.
2. En VS Code, selecciona **Archivo > Abrir carpeta** y elige `cromovital-inventario`.
3. Si VS Code pregunta por el intérprete, selecciona Python 3.10 o posterior.
4. Abre `inventario.py` y elige **Run Python File** o ejecuta `python inventario.py` en la terminal integrada.
5. Para ejecutar las pruebas, usa `python -m unittest -v`.

## Ejemplo de salida

El programa lista cada modelo y su descripción específica, muestra las existencias y calcula el valor total del inventario.

## Estructura de clases

Consulta el diagrama en `diagrama_clases.mmd` (formato Mermaid).

- `Producto` es abstracta y centraliza SKU, nombre, precio, existencias y operaciones comunes.
- `descripcion()` es abstracto; cada clase de pulsera ofrece su propia implementación.
- `Valorizable` es un `Protocol`: establece el contrato `valor_inventario()` sin exigir herencia explícita.
- `Inventario` mantiene una colección de objetos `Producto` y los procesa con métodos comunes.

## Alcance

El programa es una demostración en memoria. Al cerrar la aplicación, los cambios de stock no se guardan. En un uso real se podría añadir una base de datos, compras, ventas, reportes y control de usuarios. Las piedras se describen como materiales; no se atribuyen propiedades médicas o terapéuticas.

## GitHub

Repositorio privado: <https://github.com/Mayrisis/Cromovital_Inventario>

La rama de trabajo publicada es `feature/inventario-cromovital`. El historial incluye el commit inicial del inventario. No incluyas contraseñas ni tokens en los archivos.
