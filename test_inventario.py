"""Pruebas automatizadas de inventario y comportamiento polimórfico."""

import unittest

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
