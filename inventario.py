"""Inventario didáctico para las pulseras de piedras naturales Cromovital."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Protocol


class Valorizable(Protocol):
    """Contrato (interfaz estructural) para artículos con valor de inventario."""

    def valor_inventario(self) -> float:
        """Devuelve el valor monetario de todas las unidades disponibles."""
        ...


@dataclass
class Producto(ABC):
    """Clase abstracta con datos y operaciones que comparten los productos."""

    sku: str
    nombre: str
    precio: float
    existencias: int
    piedra: str
    diametro_mm: int = 8

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("El SKU no puede estar vacío.")
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.existencias < 0:
            raise ValueError("Las existencias no pueden ser negativas.")
        if self.diametro_mm <= 0:
            raise ValueError("El diámetro debe ser mayor que cero.")

    @abstractmethod
    def descripcion(self) -> str:
        """Cada tipo concreto describe sus materiales de forma particular."""

    def valor_inventario(self) -> float:
        """Calcula el valor de existencias; sirve igual para cualquier subtipo."""
        return round(self.precio * self.existencias, 2)

    def agregar_existencias(self, cantidad: int) -> None:
        """Repone unidades sin permitir cantidades nulas o negativas."""
        if cantidad <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor que cero.")
        self.existencias += cantidad

    def vender(self, cantidad: int) -> None:
        """Descuenta una venta cuando hay unidades suficientes."""
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self.existencias:
            raise ValueError(f"Stock insuficiente para {self.sku}.")
        self.existencias -= cantidad


class PulseraAmatista(Producto):
    """Pulsera de amatista; implementa el método abstracto heredado."""

    def descripcion(self) -> str:
        return f"Amatista natural, cuentas de {self.diametro_mm} mm, hilo elástico."


class PulseraCuarzoRosa(Producto):
    """Pulsera de cuarzo rosa con ensamble elástico."""

    def descripcion(self) -> str:
        return f"Cuarzo rosa natural, cuentas de {self.diametro_mm} mm, hilo elástico."


class PulseraObsidiana(Producto):
    """Pulsera de obsidiana con ensamble elástico."""

    def descripcion(self) -> str:
        return f"Obsidiana natural, cuentas de {self.diametro_mm} mm, hilo elástico."


class Inventario:
    """Administra productos, entradas, ventas y un historial básico."""

    def __init__(self) -> None:
        self._productos: dict[str, Producto] = {}
        self._movimientos: list[dict[str, str | int | float]] = []

    def registrar(self, producto: Producto) -> None:
        """Agrega un producto y rechaza SKU repetidos."""
        if producto.sku in self._productos:
            raise ValueError(f"El SKU {producto.sku} ya está registrado.")
        self._productos[producto.sku] = producto

    def buscar(self, sku: str) -> Producto:
        """Busca por SKU e informa claramente si no existe."""
        try:
            return self._productos[sku]
        except KeyError as error:
            raise KeyError(f"No existe un producto con SKU {sku}.") from error

    def listar(self) -> list[Producto]:
        """Entrega los productos para procesarlos polimórficamente."""
        return list(self._productos.values())

    def valor_total(self) -> float:
        """Suma el mismo método de interfaz para cada producto."""
        articulos: list[Valorizable] = self.listar()
        return round(sum(articulo.valor_inventario() for articulo in articulos), 2)

    def registrar_entrada(self, sku: str, cantidad: int) -> None:
        """Registra una reposición y la agrega al historial de movimientos."""
        producto = self.buscar(sku)
        producto.agregar_existencias(cantidad)
        self._guardar_movimiento("ENTRADA", producto, cantidad, 0)

    def vender(self, sku: str, cantidad: int) -> float:
        """Registra una venta, descuenta stock y devuelve el importe total."""
        producto = self.buscar(sku)
        producto.vender(cantidad)  # valida cantidad y stock antes del registro
        total = round(producto.precio * cantidad, 2)
        self._guardar_movimiento("VENTA", producto, cantidad, total)
        return total

    def historial(self) -> list[dict[str, str | int | float]]:
        """Devuelve una copia del historial para que el llamador no lo altere."""
        return [movimiento.copy() for movimiento in self._movimientos]

    def _guardar_movimiento(self, tipo: str, producto: Producto, cantidad: int, total: float) -> None:
        self._movimientos.append({
            "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
            "tipo": tipo,
            "sku": producto.sku,
            "producto": producto.nombre,
            "cantidad": cantidad,
            "total_mxn": total,
        })

    def guardar(self, archivo: Path) -> None:
        """Guarda productos e historial en JSON local, sin librerías externas."""
        datos = {
            "productos": [
                {
                    "tipo": _tipo_producto(producto),
                    "sku": producto.sku,
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "existencias": producto.existencias,
                    "piedra": producto.piedra,
                    "diametro_mm": producto.diametro_mm,
                }
                for producto in self.listar()
            ],
            "movimientos": self._movimientos,
        }
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def cargar(cls, archivo: Path) -> Inventario:
        """Recupera productos e historial desde el archivo JSON local."""
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        clases = {
            "amatista": PulseraAmatista,
            "cuarzo_rosa": PulseraCuarzoRosa,
            "obsidiana": PulseraObsidiana,
        }
        inventario = cls()
        for registro in datos.get("productos", []):
            clase = clases.get(registro["tipo"])
            if clase is None:
                raise ValueError(f"Tipo de pulsera desconocido: {registro['tipo']}.")
            inventario.registrar(clase(**{k: v for k, v in registro.items() if k != "tipo"}))
        inventario._movimientos = datos.get("movimientos", [])
        return inventario


def _tipo_producto(producto: Producto) -> str:
    """Traduce cada clase derivada a un identificador estable para el JSON."""
    if isinstance(producto, PulseraAmatista):
        return "amatista"
    if isinstance(producto, PulseraCuarzoRosa):
        return "cuarzo_rosa"
    if isinstance(producto, PulseraObsidiana):
        return "obsidiana"
    raise ValueError(f"No se puede guardar el tipo {type(producto).__name__}.")


def crear_inventario_demo() -> Inventario:
    """Prepara un inventario pequeño para aprender y ejecutar el ejemplo."""
    inventario = Inventario()
    inventario.registrar(PulseraAmatista("CRO-001", "Amatista clásica", 280.0, 12, "Amatista"))
    inventario.registrar(PulseraCuarzoRosa("CRO-002", "Cuarzo rosa delicado", 250.0, 8, "Cuarzo rosa", 6))
    inventario.registrar(PulseraObsidiana("CRO-003", "Obsidiana volcánica", 300.0, 5, "Obsidiana", 10))
    return inventario


def mostrar_inventario(inventario: Inventario) -> None:
    """Presenta cualquier tipo de pulsera por medio de sus métodos comunes."""
    print("\nSKU | Producto | Tipo y materiales | Precio | Stock")
    for producto in inventario.listar():
        # Python selecciona descripcion() de la clase derivada de cada objeto.
        print(f"{producto.sku} | {producto.nombre} | {producto.descripcion()} | "
              f"${producto.precio:,.2f} | {producto.existencias}")
    print(f"Valor total en existencias: ${inventario.valor_total():,.2f} MXN")


def main() -> None:
    """Menú para registrar pulseras, recibir stock y cobrar ventas."""
    archivo = Path(__file__).with_name("datos_cromovital.json")
    inventario = Inventario.cargar(archivo) if archivo.exists() else crear_inventario_demo()
    print("CROMOVITAL | Control de inventario y ventas")
    while True:
        print("\n1. Ver inventario\n2. Registrar producto\n3. Registrar entrada de stock"
              "\n4. Registrar venta\n5. Ver historial\n0. Guardar y salir")
        opcion = input("Elige una opción: ").strip()
        try:
            if opcion == "1":
                mostrar_inventario(inventario)
            elif opcion == "2":
                _registrar_producto_interactivo(inventario)
                inventario.guardar(archivo)
            elif opcion == "3":
                sku = input("SKU: ").strip()
                cantidad = int(input("Cantidad recibida: "))
                inventario.registrar_entrada(sku, cantidad)
                inventario.guardar(archivo)
                print("Entrada guardada.")
            elif opcion == "4":
                sku = input("SKU vendido: ").strip()
                cantidad = int(input("Cantidad: "))
                total = inventario.vender(sku, cantidad)
                inventario.guardar(archivo)
                print(f"Venta registrada. Total a cobrar: ${total:,.2f} MXN")
            elif opcion == "5":
                for movimiento in inventario.historial():
                    print("{fecha} | {tipo} | {sku} {producto} | {cantidad} pza | ${total_mxn:,.2f}"
                          .format(**movimiento))
                if not inventario.historial():
                    print("Todavía no hay movimientos.")
            elif opcion == "0":
                inventario.guardar(archivo)
                print(f"Datos guardados en {archivo.name}. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida.")
        except (ValueError, KeyError, OSError) as error:
            print(f"No se pudo completar la operación: {error}")


def _registrar_producto_interactivo(inventario: Inventario) -> None:
    """Solicita datos en consola y crea la subclase adecuada de pulsera."""
    tipos = {"1": PulseraAmatista, "2": PulseraCuarzoRosa, "3": PulseraObsidiana}
    print("Tipo: 1. Amatista  2. Cuarzo rosa  3. Obsidiana")
    clase = tipos.get(input("Elige tipo: ").strip())
    if clase is None:
        raise ValueError("Tipo de pulsera no válido.")
    producto = clase(
        sku=input("SKU único: ").strip(),
        nombre=input("Nombre del modelo: ").strip(),
        precio=float(input("Precio en MXN: ")),
        existencias=int(input("Existencias iniciales: ")),
        piedra=clase.__name__.replace("Pulsera", ""),
        diametro_mm=int(input("Diámetro de cuentas en mm (ej. 8): ")),
    )
    inventario.registrar(producto)
    print(f"Producto {producto.sku} registrado.")


if __name__ == "__main__":
    main()
