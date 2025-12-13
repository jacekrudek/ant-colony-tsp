import pytest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.map.pheromone_matrix import PheromoneMatrix


class TestPheromoneMatrix:
    def test_initialization(self):
        """Test PheromoneMatrix initialization"""
        pm = PheromoneMatrix(vertex_count=3, evaporation_rate=0.7)
        
        assert pm.vertex_count == 3
        assert pm.evaporation_rate == 0.7
        
        # Check current matrix structure and values
        assert len(pm.current) == 3
        for i in range(3):
            assert len(pm.current[i]) == 3
            for j in range(3):
                if i == j:
                    assert pm.current[i][j] == 0.0
                else:
                    assert pm.current[i][j] == 1.0
        
        # Check pending matrix structure and values
        assert len(pm.pending) == 3
        for i in range(3):
            assert len(pm.pending[i]) == 3
            for j in range(3):
                assert pm.pending[i][j] == 0.0

    def test_init_pheromones_custom_level(self):
        """Test init_pheromones with custom level"""
        pm = PheromoneMatrix(vertex_count=2, evaporation_rate=0.5)
        
        matrix = pm.init_pheromones(2.5)
        
        assert len(matrix) == 2
        for i in range(2):
            assert len(matrix[i]) == 2
            for j in range(2):
                if i == j:
                    assert matrix[i][j] == 0.0
                else:
                    assert matrix[i][j] == 2.5

    def test_reset_pending(self):
        """Test reset_pending sets all pending values to 0"""
        pm = PheromoneMatrix(vertex_count=2, evaporation_rate=0.5)
        
        # Set some pending values
        pm.pending[0][1] = 3.5
        pm.pending[1][0] = 2.1
        
        pm.reset_pending()
        
        # All pending should be 0.0
        for i in range(2):
            for j in range(2):
                assert pm.pending[i][j] == 0.0

    def test_add_pending(self):
        """Test add_pending accumulates values correctly"""
        pm = PheromoneMatrix(vertex_count=2, evaporation_rate=0.5)
        
        # Add multiple values to same edge
        pm.add_pending(0, 1, 1.5)
        pm.add_pending(0, 1, 2.3)
        pm.add_pending(1, 0, 0.7)
        
        # Check accumulation
        assert pm.pending[0][1] == pytest.approx(3.8)  # 1.5 + 2.3
        assert pm.pending[1][0] == pytest.approx(0.7)
        assert pm.pending[0][0] == 0.0  # Unchanged
        assert pm.pending[1][1] == 0.0  # Unchanged

    def test_apply_pending_evaporation_and_addition(self):
        """Test apply_pending does evaporation and adds pending values"""
        pm = PheromoneMatrix(vertex_count=2, evaporation_rate=0.8)
        
        # Set known current values
        pm.current[0][1] = 5.0
        pm.current[1][0] = 3.0
        
        # Set pending values
        pm.pending[0][1] = 2.0
        pm.pending[1][0] = 1.5
        
        pm.apply_pending()
        
        # Check: new = (old * evaporation_rate) + pending
        assert pm.current[0][1] == pytest.approx(6.0)  # (5.0 * 0.8) + 2.0 = 4.0 + 2.0
        assert pm.current[1][0] == pytest.approx(3.9)  # (3.0 * 0.8) + 1.5 = 2.4 + 1.5
        
        # Diagonal should remain 0.0
        assert pm.current[0][0] == 0.0
        assert pm.current[1][1] == 0.0
        
        # Pending should be reset to 0.0
        for i in range(2):
            for j in range(2):
                assert pm.pending[i][j] == 0.0

    def test_full_update_cycle(self):
        """Test complete pheromone update cycle"""
        pm = PheromoneMatrix(vertex_count=2, evaporation_rate=0.9)
        
        # Initial state
        initial_value = pm.current[0][1]
        assert initial_value == 1.0
        
        # Add some pheromone
        pm.add_pending(0, 1, 0.5)
        
        # Apply changes
        pm.apply_pending()
        
        # Expected: (1.0 * 0.9) + 0.5 = 1.4
        assert pm.current[0][1] == pytest.approx(1.4)
        assert pm.pending[0][1] == 0.0
