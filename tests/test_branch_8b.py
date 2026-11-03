# Тесты ветви 8b: единицы измерения.
# На каждый метод: обычный, граничный и ошибочный случай
# (у методов без исключений третий случай — ещё одна граница).

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_8b_units import (
    is_length_unit, length_factor, is_mass_unit, mass_factor,
    is_volume_unit, volume_factor, linear_convert, convert_length,
    convert_mass, convert_volume, celsius_to_kelvin, kelvin_to_celsius,
    celsius_to_fahrenheit, fahrenheit_to_celsius, is_temperature_unit,
    to_celsius, from_celsius, convert_temperature, convert_unit,
)


class TestIsLengthUnit(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(is_length_unit("km"), True)

    def test_boundary(self):
        self.assertEqual(is_length_unit("mm"), True)
        self.assertEqual(is_length_unit("kg"), False)

    def test_error(self):
        self.assertEqual(is_length_unit("mile"), False)


class TestLengthFactor(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(length_factor("km"), 1000.0)

    def test_boundary(self):
        self.assertAlmostEqual(length_factor("mm"), 0.001)
        self.assertEqual(length_factor("m"), 1.0)

    def test_error(self):
        with self.assertRaises(ValueError):
            length_factor("mi")


class TestIsMassUnit(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(is_mass_unit("kg"), True)

    def test_boundary(self):
        self.assertEqual(is_mass_unit("mg"), True)
        self.assertEqual(is_mass_unit("m"), False)

    def test_error(self):
        self.assertEqual(is_mass_unit("pound"), False)


class TestMassFactor(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(mass_factor("t"), 1000000.0)

    def test_boundary(self):
        self.assertAlmostEqual(mass_factor("mg"), 0.001)
        self.assertEqual(mass_factor("g"), 1.0)

    def test_error(self):
        with self.assertRaises(ValueError):
            mass_factor("lb")


class TestIsVolumeUnit(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(is_volume_unit("l"), True)

    def test_boundary(self):
        self.assertEqual(is_volume_unit("ml"), True)
        self.assertEqual(is_volume_unit("m"), False)

    def test_error(self):
        self.assertEqual(is_volume_unit("gallon"), False)


class TestVolumeFactor(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(volume_factor("kl"), 1000.0)

    def test_boundary(self):
        self.assertAlmostEqual(volume_factor("ml"), 0.001)
        self.assertEqual(volume_factor("l"), 1.0)

    def test_error(self):
        with self.assertRaises(ValueError):
            volume_factor("pt")


class TestLinearConvert(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(linear_convert(2, 1000.0, 1.0), 2000.0)

    def test_boundary(self):
        self.assertEqual(linear_convert(0, 1000.0, 0.001), 0.0)
        self.assertAlmostEqual(linear_convert(-5, 1000.0, 1.0), -5000.0)

    def test_error(self):
        # Дробные коэффициенты: отношение считается в обе стороны.
        self.assertAlmostEqual(linear_convert(1, 0.001, 1000.0), 0.000001)


class TestConvertLength(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(convert_length(2, "km", "m"), 2000.0)

    def test_boundary(self):
        self.assertEqual(convert_length(0, "mm", "km"), 0.0)
        self.assertAlmostEqual(convert_length(1, "mm", "m"), 0.001)

    def test_error(self):
        with self.assertRaises(ValueError):
            convert_length(2, "km", "kg")


class TestConvertMass(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(convert_mass(1, "t", "kg"), 1000.0)

    def test_boundary(self):
        self.assertEqual(convert_mass(0, "mg", "t"), 0.0)
        self.assertAlmostEqual(convert_mass(1, "g", "t"), 0.000001)

    def test_error(self):
        with self.assertRaises(ValueError):
            convert_mass(1, "kg", "km")


class TestConvertVolume(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(convert_volume(1, "l", "ml"), 1000.0)

    def test_boundary(self):
        self.assertEqual(convert_volume(0, "ml", "kl"), 0.0)
        self.assertAlmostEqual(convert_volume(1, "ml", "l"), 0.001)

    def test_error(self):
        with self.assertRaises(ValueError):
            convert_volume(1, "l", "m")


class TestCelsiusToKelvin(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(celsius_to_kelvin(0), 273.15)

    def test_boundary(self):
        self.assertAlmostEqual(celsius_to_kelvin(-273.15), 0.0)

    def test_error(self):
        # Обратная точка: 273.15 C не определено физикой, метод не ограничивает.
        self.assertAlmostEqual(celsius_to_kelvin(100), 373.15)


class TestKelvinToCelsius(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0.0)

    def test_boundary(self):
        self.assertAlmostEqual(kelvin_to_celsius(0), -273.15)

    def test_error(self):
        self.assertAlmostEqual(kelvin_to_celsius(373.15), 100.0)


class TestCelsiusToFahrenheit(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212.0)

    def test_boundary(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40.0)

    def test_error(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.6)


class TestFahrenheitToCelsius(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100.0)

    def test_boundary(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40), -40.0)

    def test_error(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(98.6), 37.0)


class TestIsTemperatureUnit(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(is_temperature_unit("c"), True)

    def test_boundary(self):
        self.assertEqual(is_temperature_unit("k"), True)
        self.assertEqual(is_temperature_unit("m"), False)

    def test_error(self):
        self.assertEqual(is_temperature_unit("r"), False)


class TestToCelsius(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(to_celsius(212, "f"), 100.0)
        self.assertEqual(to_celsius(5, "c"), 5)

    def test_boundary(self):
        self.assertAlmostEqual(to_celsius(-40, "f"), -40.0)
        self.assertAlmostEqual(to_celsius(0, "k"), -273.15)

    def test_error(self):
        with self.assertRaises(ValueError):
            to_celsius(100, "x")


class TestFromCelsius(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(from_celsius(100, "f"), 212.0)
        self.assertEqual(from_celsius(5, "c"), 5)

    def test_boundary(self):
        self.assertAlmostEqual(from_celsius(-40, "f"), -40.0)
        self.assertAlmostEqual(from_celsius(0, "k"), 273.15)

    def test_error(self):
        with self.assertRaises(ValueError):
            from_celsius(100, "x")


class TestConvertTemperature(unittest.TestCase):
    def test_usual(self):
        self.assertAlmostEqual(convert_temperature(100, "c", "f"), 212.0)

    def test_boundary(self):
        self.assertAlmostEqual(convert_temperature(-40, "f", "c"), -40.0)
        self.assertAlmostEqual(convert_temperature(0, "c", "k"), 273.15)

    def test_error(self):
        self.assertAlmostEqual(convert_temperature(300, "k", "c"), 26.85)


class TestConvertUnit(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(convert_unit(100, "km", "m"), 100000.0)

    def test_boundary(self):
        self.assertAlmostEqual(convert_unit(-40, "f", "c"), -40.0)
        self.assertAlmostEqual(convert_unit(1, "t", "g"), 1000000.0)
        self.assertAlmostEqual(convert_unit(1, "l", "ml"), 1000.0)

    def test_error(self):
        with self.assertRaises(ValueError):
            convert_unit(1, "km", "kg")
        with self.assertRaises(ValueError):
            convert_unit(1, "xx", "m")


if __name__ == "__main__":
    unittest.main()