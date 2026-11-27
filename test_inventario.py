"""Pruebas automatizadas de inventario y comportamiento polimórfico."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from inventario import (
    Inventario,
    PulseraAmatista,
    PulseraCuarzoRosa,
    PulseraObsidiana,
    Producto,
    crear_inventario_demo,
)


class PruebasInventario(unittest.TestCase):
    def test_clase_abstracta_no_se_puede_instanciar(self):
        with self.assertRaises(TypeError):
            Producto("SKU", "Producto", 10, 1, "Piedra")

    def test_polimorfismo_en_descripciones(self):
        productos = [
            PulseraAmatista("A", "Amatista", 100, 2, "Amatista"),
            PulseraCuarzoRosa("B", "Cuarzo", 120, 3, "Cuarzo rosa"),
            PulseraObsidiana("C", "Obsidiana", 90, 4, "Obsidiana"),
        ]
        descripciones = [producto.descripcion() for producto in productos]
        self.assertIn("Amatista", descripciones[0])
        self.assertIn("Cuarzo rosa", descripciones[1])
        self.assertIn("Obsidiana", descripciones[2])

    def test_valor_total_usa_un_metodo_comun(self):
        inventario = crear_inventario_demo()
        self.assertEqual(inventario.valor_total(), 6860.0)

    def test_venta_y_reposicion(self):
        producto = PulseraAmatista("A", "Amatista", 100, 5, "Amatista")
        producto.vender(2)
        producto.agregar_existencias(4)
        self.assertEqual(producto.existencias, 7)
        self.assertEqual(producto.valor_inventario(), 700.0)

    def test_no_permite_vender_mas_del_stock(self):
        producto = PulseraObsidiana("O", "Obsidiana", 90, 1, "Obsidiana")
        with self.assertRaises(ValueError):
            producto.vender(2)

    def test_rechaza_sku_duplicado(self):
        inventario = Inventario()
        inventario.registrar(PulseraAmatista("A", "Una", 100, 2, "Amatista"))
        with self.assertRaises(ValueError):
            inventario.registrar(PulseraCuarzoRosa("A", "Dos", 120, 3, "Cuarzo rosa"))

    def test_rechaza_datos_invalidos(self):
        with self.assertRaises(ValueError):
            PulseraAmatista("A", "Amatista", -1, 2, "Amatista")
        with self.assertRaises(ValueError):
            PulseraAmatista("B", "Amatista", 100, -1, "Amatista")

    def test_venta_registra_movimiento_y_descuenta_stock(self):
        inventario = crear_inventario_demo()
        total = inventario.vender("CRO-001", 2)
        self.assertEqual(total, 560.0)
        self.assertEqual(inventario.buscar("CRO-001").existencias, 10)
        self.assertEqual(inventario.historial()[-1]["tipo"], "VENTA")

    def test_entrada_registra_movimiento_y_aumenta_stock(self):
        inventario = crear_inventario_demo()
        inventario.registrar_entrada("CRO-002", 3)
        self.assertEqual(inventario.buscar("CRO-002").existencias, 11)
        self.assertEqual(inventario.historial()[-1]["tipo"], "ENTRADA")

    def test_no_registra_venta_si_el_stock_no_alcanza(self):
        inventario = crear_inventario_demo()
        with self.assertRaises(ValueError):
            inventario.vender("CRO-003", 99)
        self.assertEqual(inventario.historial(), [])

    def test_persistencia_conserva_productos_y_movimientos(self):
        inventario = crear_inventario_demo()
        inventario.vender("CRO-001", 1)
        with TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "datos.json"
            inventario.guardar(archivo)
            recuperado = Inventario.cargar(archivo)
        self.assertEqual(recuperado.buscar("CRO-001").existencias, 11)
        self.assertEqual(recuperado.historial()[0]["tipo"], "VENTA")


if __name__ == "__main__":
    unittest.main(verbosity=2)
