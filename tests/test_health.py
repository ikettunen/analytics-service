"""
Analytics Service - Health Endpoint Tests
Test Suite: S5.TS1

Tests the health check endpoint to ensure the service is running
and responding correctly.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """S5.TS1: Health Endpoint Tests"""
    
    def test_health_returns_200_with_service_name(self):
        """
        Test: S5.TS1.1
        Verify that the health endpoint returns 200 status with correct service name
        
        Expected behavior:
        - Status code should be 200
        - Response should contain status: 'ok'
        - Response should contain service: 'analytics-service'
        """
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "analytics-service"
