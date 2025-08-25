"""
Test script to validate BTG Pactual API functionality
Run this after starting the application with start.bat
"""

import asyncio
import httpx
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"


class BTGPactualTester:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.admin_token = None
        self.user_token = None
        self.fund_id = None
        
    async def close(self):
        await self.client.aclose()
    
    def print_result(self, test_name: str, success: bool, details: str = ""):
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        print()
    
    async def test_health_check(self):
        """Test if the API is running"""
        try:
            response = await self.client.get(f"{BASE_URL}/health")
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Services: {list(data.get('services', {}).keys())}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("Health Check", success, details)
        return success
    
    async def test_admin_login(self):
        """Test admin login"""
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": "admin@btgpactual.com",
                    "password": "Admin123!"
                }
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                self.admin_token = data["access_token"]
                details = f"Token received: {self.admin_token[:20]}..."
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("Admin Login", success, details)
        return success
    
    async def test_user_registration(self):
        """Test user registration"""
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/register",
                json={
                    "email": "test.user@btgpactual.com",
                    "password": "Test123!",
                    "full_name": "Usuario de Prueba",
                    "phone_number": "+57300123456"
                }
            )
            success = response.status_code in [200, 201]
            if success:
                data = response.json()
                details = f"User created: {data.get('email', 'N/A')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("User Registration", success, details)
        return success
    
    async def test_user_login(self):
        """Test user login"""
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": "test.user@btgpactual.com",
                    "password": "Test123!"
                }
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                self.user_token = data["access_token"]
                details = f"Token received: {self.user_token[:20]}..."
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("User Login", success, details)
        return success
    
    async def test_get_funds(self):
        """Test getting available funds"""
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"} if self.user_token else {}
            response = await self.client.get(f"{API_BASE}/funds/", headers=headers)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                funds = data.get("data", [])
                if funds:
                    self.fund_id = funds[0]["id"]
                    details = f"Found {len(funds)} funds. First fund: {funds[0]['name']}"
                else:
                    details = "No funds found"
                    success = False
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("Get Funds", success, details)
        return success
    
    async def test_fund_subscription(self):
        """Test fund subscription"""
        if not self.user_token or not self.fund_id:
            self.print_result("Fund Subscription", False, "Missing user token or fund ID")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = await self.client.post(
                f"{API_BASE}/funds/subscribe",
                headers=headers,
                json={
                    "fund_id": self.fund_id,
                    "amount": 100000
                }
            )
            success = response.status_code in [200, 201]
            
            if success:
                data = response.json()
                details = f"Subscription created: {data.get('message', 'Success')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("Fund Subscription", success, details)
        return success
    
    async def test_get_user_profile(self):
        """Test getting user profile"""
        if not self.user_token:
            self.print_result("Get User Profile", False, "Missing user token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = await self.client.get(f"{API_BASE}/users/me", headers=headers)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                user_data = data.get("data", {})
                details = f"User: {user_data.get('email', 'N/A')}, Balance: ${user_data.get('current_balance', 'N/A')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("Get User Profile", success, details)
        return success
    
    async def test_transaction_history(self):
        """Test getting transaction history"""
        if not self.user_token:
            self.print_result("Transaction History", False, "Missing user token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = await self.client.get(f"{API_BASE}/transactions/history", headers=headers)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transactions = data.get("data", [])
                details = f"Found {len(transactions)} transactions"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.print_result("Transaction History", success, details)
        return success
    
    async def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 Iniciando pruebas de BTG Pactual API...")
        print("=" * 50)
        print()
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Admin Login", self.test_admin_login),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Get Funds", self.test_get_funds),
            ("Fund Subscription", self.test_fund_subscription),
            ("Get User Profile", self.test_get_user_profile),
            ("Transaction History", self.test_transaction_history),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            result = await test_func()
            if result:
                passed += 1
        
        print("=" * 50)
        print(f"🏁 Pruebas completadas: {passed}/{total} exitosas")
        
        if passed == total:
            print("🎉 ¡Todas las pruebas pasaron! La API está funcionando correctamente.")
        else:
            print("⚠️  Algunas pruebas fallaron. Verifica la configuración y los logs.")


async def main():
    tester = BTGPactualTester()
    try:
        await tester.run_all_tests()
    finally:
        await tester.close()


if __name__ == "__main__":
    print("BTG Pactual API - Suite de Pruebas")
    print("Asegúrate de que la API esté ejecutándose en http://localhost:8000")
    print()
    
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())
