"""
Analytics Service - Patient Analytics Tests
Test Suite: S5.TS2

Tests patient analytics endpoints including patient summaries
and critical patient counts.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


class TestPatientAnalytics:
    """S5.TS2: Patient Analytics Tests"""
    
    def test_patients_summary_returns_count_by_status(self):
        """
        Test: S5.TS2.1
        Verify that patients summary returns patient count grouped by status
        
        Expected behavior:
        - Status code should be 200
        - Response should contain data array
        - Each item should have status and count fields
        """
        response = client.get("/api/analytics/patients/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        
        # If data exists, verify structure
        if len(data["data"]) > 0:
            item = data["data"][0]
            assert "status" in item
            assert "count" in item
            assert isinstance(item["count"], int)
    
    def test_critical_patients_returns_count(self):
        """
        Test: S5.TS2.2
        Verify that critical patients endpoint returns count of critical patients
        
        Expected behavior:
        - Status code should be 200
        - Response should contain data object
        - Data should have critical_patients field with integer value
        """
        response = client.get("/api/analytics/patients/critical")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "critical_patients" in data["data"]
        assert isinstance(data["data"]["critical_patients"], int)
        assert data["data"]["critical_patients"] >= 0
    
    def test_patient_counts_are_accurate(self):
        """
        Test: S5.TS2.3
        Verify that patient counts are accurate and consistent
        
        Expected behavior:
        - Counts should be non-negative integers
        - Total from summary should be consistent
        - Critical count should be <= total count
        """
        # Get summary
        summary_response = client.get("/api/analytics/patients/summary")
        assert summary_response.status_code == 200
        summary_data = summary_response.json()["data"]
        
        # Get critical count
        critical_response = client.get("/api/analytics/patients/critical")
        assert critical_response.status_code == 200
        critical_count = critical_response.json()["data"]["critical_patients"]
        
        # Verify all counts are non-negative
        for item in summary_data:
            assert item["count"] >= 0
        
        # Calculate total from summary
        total_from_summary = sum(item["count"] for item in summary_data)
        
        # Critical count should not exceed total
        assert critical_count <= total_from_summary or total_from_summary == 0
