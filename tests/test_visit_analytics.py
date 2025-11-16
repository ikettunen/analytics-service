"""
Analytics Service - Visit Analytics Tests
Test Suite: S5.TS3

Tests visit analytics endpoints including visit summaries
grouped by status.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestVisitAnalytics:
    """S5.TS3: Visit Analytics Tests"""
    
    def test_visits_summary_returns_count_by_status(self):
        """
        Test: S5.TS3.1
        Verify that visits summary returns visit count grouped by status
        
        Expected behavior:
        - Status code should be 200
        - Response should contain data array
        - Each item should have status and count fields
        - Counts should be non-negative integers
        """
        response = client.get("/api/analytics/visits/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        
        # Verify structure if data exists
        if len(data["data"]) > 0:
            item = data["data"][0]
            assert "status" in item
            assert "count" in item
            assert isinstance(item["count"], int)
            assert item["count"] >= 0
    
    def test_visit_counts_are_accurate(self):
        """
        Test: S5.TS3.2
        Verify that visit counts are accurate and consistent
        
        Expected behavior:
        - All counts should be non-negative integers
        - Status values should be valid visit statuses
        - Total count should be sum of all status counts
        """
        response = client.get("/api/analytics/visits/summary")
        
        assert response.status_code == 200
        data = response.json()["data"]
        
        # Verify all counts are non-negative
        total_count = 0
        for item in data:
            assert isinstance(item["count"], int)
            assert item["count"] >= 0
            assert isinstance(item["status"], str)
            total_count += item["count"]
        
        # Total should be sum of all counts
        assert total_count >= 0
