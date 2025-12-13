import pytest
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.map.graph import Graph
from src.map.vertice import Vertice

class TestGraph:
    def test_initialization(self):
        """Test Graph initialization with correct number of vertices"""
        graph = Graph(5)
        
        assert graph.num_vertices == 5
        assert len(graph.vertices) == 5
        assert graph.best_path is None
        assert graph.best_path_length == float('inf')
        assert graph.last_iteration_paths == []
        
        # Check that all vertices are Vertice instances
        for vertex in graph.vertices:
            assert isinstance(vertex, Vertice)

    def test_vertices_have_valid_coordinates(self):
        """Test that generated vertices have valid coordinates"""
        from src.config import CENTER_WIDTH, SCREEN_HEIGHT
        
        graph = Graph(10)
        
        for vertex in graph.vertices:
            assert 0 <= vertex.x < CENTER_WIDTH - 20
            assert 0 <= vertex.y < SCREEN_HEIGHT - 20

    def test_distance_matrix_structure(self):
        """Test distance matrix has correct structure"""
        graph = Graph(3)
        
        # Should be dict of dicts
        assert isinstance(graph.distance_matrix, dict)
        assert len(graph.distance_matrix) == 3
        
        # Each row should have 3 columns
        for i in range(3):
            assert i in graph.distance_matrix
            assert len(graph.distance_matrix[i]) == 3
            
            # Diagonal should be 0
            assert graph.distance_matrix[i][i] == 0.0
            
            # Distance should be symmetric
            for j in range(3):
                if i != j:
                    assert graph.distance_matrix[i][j] > 0.0
                    assert graph.distance_matrix[i][j] == graph.distance_matrix[j][i]

    def test_get_edge_grade_calculation(self):
        """Test edge grade calculation (1/distance)"""
        graph = Graph(2)
        
        # Get actual distance between vertices 0 and 1
        distance = graph.distance_matrix[0][1]
        edge_grade = graph.get_edge_grade(0, 1)
        
        # Edge grade should be 1/distance
        assert edge_grade == pytest.approx(1.0 / distance)

    def test_get_edge_grade_zero_distance(self):
        """Test edge grade with zero distance (same vertex)"""
        graph = Graph(3)
        
        # Distance from vertex to itself should be 0
        assert graph.distance_matrix[0][0] == 0.0
        
        # Edge grade should be 0 for zero distance
        edge_grade = graph.get_edge_grade(0, 0)
        assert edge_grade == 0.0

    def test_rebuild_resets_state(self):
        """Test that rebuild resets graph state"""
        graph = Graph(3)
        
        # Set some state
        graph.best_path = [0, 1, 2]
        graph.best_path_length = 15.5
        graph.last_iteration_paths = [([0, 1, 2], 20.0)]
        
        # Rebuild should reset state
        graph.rebuild()
        
        assert graph.best_path is None
        assert graph.best_path_length == float('inf')
        assert graph.last_iteration_paths == []
        
        # Distance matrix should still exist and be valid
        assert graph.distance_matrix is not None
        assert len(graph.distance_matrix) == 3

    def test_calculate_distances_creates_valid_matrix(self):
        """Test that calculate_distances creates valid distance matrix"""
        graph = Graph(4)
        
        # Manually call calculate_distances
        graph.calculate_distances()
        
        # Check matrix properties
        for i in range(4):
            for j in range(4):
                if i == j:
                    assert graph.distance_matrix[i][j] == 0.0
                else:
                    # Distance should be positive and symmetric
                    assert graph.distance_matrix[i][j] > 0.0
                    assert graph.distance_matrix[i][j] == graph.distance_matrix[j][i]

    def test_single_vertex_graph(self):
        """Test graph with single vertex"""
        graph = Graph(1)
        
        assert graph.num_vertices == 1
        assert len(graph.vertices) == 1
        assert len(graph.distance_matrix) == 1
        assert graph.distance_matrix[0][0] == 0.0
        
        # Edge grade to itself should be 0
        assert graph.get_edge_grade(0, 0) == 0.0

    def test_distance_calculation_with_known_vertices(self):
        """Test distance calculation with specific vertex coordinates"""
        
        # Create graph with known vertices
        graph = Graph(3)
        
        # Override vertices with known coordinates
        graph.vertices = [
            Vertice(0, 0),    # vertex 0 at origin
            Vertice(3, 4),    # vertex 1 at (3, 4) - creates 3-4-5 triangle
            Vertice(6, 0)     # vertex 2 at (6, 0) - horizontal line
        ]
        
        # Recalculate distances with new vertices
        graph.calculate_distances()
        
        # Check specific distance calculations
        # Distance from (0,0) to (3,4) should be 5 (3-4-5 triangle)
        assert graph.distance_matrix[0][1] == pytest.approx(5.0)
        assert graph.distance_matrix[1][0] == pytest.approx(5.0)
        
        # Distance from (0,0) to (6,0) should be 6 (horizontal line)
        assert graph.distance_matrix[0][2] == pytest.approx(6.0)
        assert graph.distance_matrix[2][0] == pytest.approx(6.0)
        
        # Distance from (3,4) to (6,0) should be sqrt((6-3)² + (0-4)²) = sqrt(9+16) = 5
        assert graph.distance_matrix[1][2] == pytest.approx(5.0)
        assert graph.distance_matrix[2][1] == pytest.approx(5.0)
        
        # Diagonal should be 0
        assert graph.distance_matrix[0][0] == 0.0
        assert graph.distance_matrix[1][1] == 0.0
        assert graph.distance_matrix[2][2] == 0.0

    def test_edge_grade_with_known_distances(self):
        """Test edge grade calculation with known vertex coordinates"""
        
        graph = Graph(2)
        
        # Set vertices: distance should be 10
        graph.vertices = [
            Vertice(0, 0),    # vertex 0
            Vertice(6, 8)     # vertex 1 - creates 6-8-10 triangle
        ]
        
        graph.calculate_distances()
        
        # Distance should be 10
        assert graph.distance_matrix[0][1] == pytest.approx(10.0)
        
        # Edge grade should be 1/10 = 0.1
        edge_grade = graph.get_edge_grade(0, 1)
        assert edge_grade == pytest.approx(0.1)