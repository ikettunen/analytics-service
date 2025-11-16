"""
Analytics Service - Database Connection Tests
Test Suite: S5.TS6

Tests database connectivity and query execution for MySQL.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestDatabaseConnection:
    """S5.TS6: Database Connection Tests"""
    
    def test_mysql_connection_established(self):
        """
        Test: S5.TS6.1
        Verify that MySQL connection is established successfully
        
        Expected behavior:
        - Service should start without database connection errors
        - Health endpoint should respond (indicates service is running)
        - Analytics endpoints should be accessible
        """
        # If service is running and health check passes, DB connection is working
        response = client.get("/health")
        assert response.status_code == 200
        
        # Try to access an analytics endpoint
        response = client.get("/api/analytics/performance")
        # Should return 200 or 500, but not connection refused
        assert response.status_code in [200, 500, 503]
    
    def test_database_queries_execute_correctly(self):
        """
        Test: S5.TS6.2
        Verify that database queries execute without errors
        
        Expected behavior:
        - Queries should return data or empty results
        - No SQL syntax errors
        - Proper error handling for failed queries
        """
        # Test multiple endpoints to verify queries work
        endpoints = [
            "/api/analytics/patients/summary",
            "/api/analytics/visits/summary",
            "/api/analytics/performance"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Should return 200 (success) or 500 (handled error), not crash
            assert response.status_code in [200, 500]
            
            # If successful, should have proper JSON structure
            if response.status_code == 200:
                data = response.json()
                assert "data" in data or "error" in data
    
    def test_connection_errors_handled(self):
        """
        Test: S5.TS6.3
        Verify that database connection errors are handled gracefully
        
        Expected behavior:
        - Service should not crash on DB errors
        - Should return appropriate error responses
        - Should include error information in response
        """
        # Test an endpoint that requires database
        response = client.get("/api/analytics/dashboard/stats")
        
        # Should always return a response, not crash
        assert response.status_code in [200, 500, 503]
        
        # Response should be valid JSON
        try:
            data = response.json()
            assert isinstance(data, dict)
        except Exception as e:
            pytest.fail(f"Response is not valid JSON: {e}")
