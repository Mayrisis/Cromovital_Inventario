"""Inventario didáctico para las pulseras de piedras naturales Cromovital."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
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
    """Administra productos sin depender de una clase de pulsera concreta."""

    def __init__(self) -> None:
        self._productos: dict[str, Producto] = {}

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


def crear_inventario_demo() -> Inventario:
    """Prepara un inventario pequeño para aprender y ejecutar el ejemplo."""
    inventario = Inventario()
    inventario.registrar(PulseraAmatista("CRO-001", "Amatista clásica", 280.0, 12, "Amatista"))
    inventario.registrar(PulseraCuarzoRosa("CRO-002", "Cuarzo rosa delicado", 250.0, 8, "Cuarzo rosa", 6))
    inventario.registrar(PulseraObsidiana("CRO-003", "Obsidiana volcánica", 300.0, 5, "Obsidiana", 10))
    return inventario


def main() -> None:
    """Muestra descripciones y valores usando una sola rutina para todos."""
    inventario = crear_inventario_demo()
    print("CROMOVITAL | Inventario de pulseras naturales")
    print("=" * 54)
    for producto in inventario.listar():
        # Python elige la descripción de la subclase según el objeto concreto.
        print(f"{producto.sku} | {producto.nombre} | {producto.descripcion()}")
        print(f"  Stock: {producto.existencias} | Valor: ${producto.valor_inventario():,.2f} MXN")
    print("-" * 54)
    print(f"Valor total del inventario: ${inventario.valor_total():,.2f} MXN")


if __name__ == "__main__":
    main()
