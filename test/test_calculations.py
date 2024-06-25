
# test_calculations.py
# Contains unit tests for the calculation logic in the RoomCalc application

import unittest
from calculations import calculate_heat_gain_from_surfaces, calculate_heat_gain_from_personnel, calculate_total_heat_gain
from models import Surface, Personnel

class TestCalculations(unittest.TestCase):
    def test_calculate_heat_gain_from_surfaces(self):
        """Test the heat gain calculation from surfaces."""
        surfaces = [
            Surface(Area=10, UValue=0.25, TemperatureOther=30),
            Surface(Area=20, UValue=0.35, TemperatureOther=25)
        ]
        expected_heat_gain = (10 * 0.25 * (30 - 20)) + (20 * 0.35 * (25 - 20))
        result = calculate_heat_gain_from_surfaces(surfaces)
        self.assertAlmostEqual(result, expected_heat_gain, places=2)

    def test_calculate_heat_gain_from_personnel(self):
        """Test the heat gain calculation from personnel."""
        personnel = [
            Personnel(Quantity=3, HeatLoadPerPersonSummer=100),
            Personnel(Quantity=2, HeatLoadPerPersonSummer=150)
        ]
        expected_heat_gain = (3 * 100) + (2 * 150)
        result = calculate_heat_gain_from_personnel(personnel)
        self.assertEqual(result, expected_heat_gain)

    def test_calculate_total_heat_gain(self):
        """Test the total heat gain calculation integrating multiple sources."""
        surfaces = [Surface(Area=15, UValue=0.30, TemperatureOther=28)]
        personnel = [Personnel(Quantity=4, HeatLoadPerPersonSummer=120)]
        lights = [Light(HeatLoadSummer=500, ApplySummer=True)]
        equipment = [Equipment(HeatLoadSummer=800, ApplySummer=True)]

        expected_heat_gain = (15 * 0.30 * (28 - 20)) + (4 * 120) + 500 + 800
        result = calculate_total_heat_gain(surfaces, personnel, lights, equipment)
        self.assertAlmostEqual(result, expected_heat_gain, places=2)

if __name__ == '__main__':
    unittest.main()

