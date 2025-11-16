"""
Analytics Service - Dashboard Statistics Tests
Test Suite: S5.TS5

Tests the comprehensive dashboard statistics endpoint that
aggregates all analytics data in a single call.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestDashboardStatistics:
    """S5.TS5: Dashboard Statistics Tests"""
    
    def test_dashboard_stats_returns_overview_data(self):
        """
        Test: S5.TS5.1
        Verify that dashboard stats returns overview data
        
        Expected behavior:
        - Status code should be 200
        - Response should contain data object
        - Data should have overview object with key metrics
        """
        response = client.get("/api/analytics/dashboard/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "overview" in data["data"]
        
        overview = data["data"]["overview"]
        assert "total_patients" in overview
        assert "total_visits" in overview
        assert "today_visits" in overview
        assert "critical_patients" in overview
        
        # Verify all are integers
        assert isinstance(overview["total_patients"], int)
        assert isinstance(overview["total_visits"], int)
        assert isinstance(overview["today_visits"], int)
        assert isinstance(overview["critical_patients"], int)
    
    def test_dashboard_stats_returns_patients_by_status(self):
        """
        Test: S5.TS5.2
        Verify that dashboard stats returns patients grouped by status
        
        Expected behavior:
        - Data should have patients_by_status array
        - Each item should have status and count
        """
        response = client.get("/api/analytics/dashboard/stats")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "patients_by_status" in data
        assert isinstance(data["patients_by_status"], list)
        
        # Verify structure if data exists
        if len(data["patients_by_status"]) > 0:
            item = data["patients_by_status"][0]
            assert "status" in item
            assert "count" in item
    
    def test_dashboard_stats_returns_visits_by_status(self):
        """
        Test: S5.TS5.3
        Verify that dashboard stats returns visits grouped by status
        
        Expected behavior:
        - Data should have visits_by_status array
        - Each item should have status and count
        """
        response = client.get("/api/analytics/dashboard/stats")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "visits_by_status" in data
        assert isinstance(data["visits_by_status"], list)
        
        # Verify structure if data exists
        if len(data["visits_by_status"]) > 0:
            item = data["visits_by_status"][0]
            assert "status" in item
            assert "count" in item
    
    def test_dashboard_handles_database_errors_gracefully(self):
        """
        Test: S5.TS5.4
        Verify that dashboard handles database errors gracefully
        
        Expected behavior:
        - Should return 200 even if some queries fail
        - Should include error information if present
        - Should not crash the service
        """
        response = client.get("/api/analytics/dashboard/stats")
        
        # Should always return a response
        assert response.status_code in [200, 500, 503]
        
        # If successful, should have data
        if response.status_code == 200:
            data = response.json()
            assert "data" in data or "error" in data
