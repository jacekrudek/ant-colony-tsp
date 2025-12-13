import pytest
import math
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.map.vertice import Vertice


class TestVertice:
    def test_initialization(self):
        """Test Vertice initialization with coordinates"""
        vertice = Vertice(10, 20)
        
        assert vertice.x == 10
        assert vertice.y == 20

    def test_initialization_with_negative_coordinates(self):
        """Test Vertice with negative coordinates"""
        vertice = Vertice(-5, -10)
        
        assert vertice.x == -5
        assert vertice.y == -10

    def test_initialization_with_float_coordinates(self):
        """Test Vertice with float coordinates"""
        vertice = Vertice(3.5, 7.8)
        
        assert vertice.x == 3.5
        assert vertice.y == 7.8

    def test_distance_to_same_point(self):
        """Test distance to itself should be 0"""
        vertice = Vertice(5, 10)
        
        distance = vertice.distance_to(vertice)
        
        assert distance == 0.0

    def test_distance_to_horizontal_point(self):
        """Test distance calculation for horizontal line"""
        vertice1 = Vertice(0, 5)
        vertice2 = Vertice(3, 5)
        
        distance = vertice1.distance_to(vertice2)
        
        assert distance == 3.0

    def test_distance_to_vertical_point(self):
        """Test distance calculation for vertical line"""
        vertice1 = Vertice(5, 0)
        vertice2 = Vertice(5, 4)
        
        distance = vertice1.distance_to(vertice2)
        
        assert distance == 4.0

    def test_distance_to_diagonal_point(self):
        """Test distance calculation for diagonal line (Pythagorean theorem)"""
        vertice1 = Vertice(0, 0)
        vertice2 = Vertice(3, 4)
        
        distance = vertice1.distance_to(vertice2)
        
        # 3-4-5 triangle: distance should be 5
        assert distance == 5.0

    def test_distance_is_symmetric(self):
        """Test that distance is symmetric: d(A,B) = d(B,A)"""
        vertice1 = Vertice(1, 2)
        vertice2 = Vertice(4, 6)
        
        distance1 = vertice1.distance_to(vertice2)
        distance2 = vertice2.distance_to(vertice1)
        
        assert distance1 == distance2

    def test_distance_with_negative_coordinates(self):
        """Test distance calculation with negative coordinates"""
        vertice1 = Vertice(-2, -3)
        vertice2 = Vertice(1, 1)
        
        distance = vertice1.distance_to(vertice2)
        
        # dx = 1 - (-2) = 3, dy = 1 - (-3) = 4
        # distance = sqrt(3² + 4²) = sqrt(9 + 16) = sqrt(25) = 5
        assert distance == 5.0

    def test_distance_calculation_precision(self):
        """Test distance calculation with floating point precision"""
        vertice1 = Vertice(0, 0)
        vertice2 = Vertice(1, 1)
        
        distance = vertice1.distance_to(vertice2)
        expected = math.sqrt(2)
        
        assert distance == pytest.approx(expected)

    def test_distance_large_coordinates(self):
        """Test distance calculation with large coordinates"""
        vertice1 = Vertice(1000, 2000)
        vertice2 = Vertice(1300, 2400)
        
        distance = vertice1.distance_to(vertice2)
        
        # dx = 300, dy = 400
        # distance = sqrt(300² + 400²) = sqrt(90000 + 160000) = sqrt(250000) = 500
        assert distance == 500.0