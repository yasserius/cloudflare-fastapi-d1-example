import requests
from datetime import datetime

class TestTodoAPI:
    def __init__(self):
        self.base_url = "http://localhost:8787"
        self.test_todos = []  # Keep track of created todos for cleanup

    def _create_todo(self, user_id=1, text="Test todo"):
        """Helper method to create a todo"""
        todo_data = {
            "user_id": user_id,
            "text": text
        }
        response = requests.post(f"{self.base_url}/todo", json=todo_data)
        if response.status_code == 200:
            self.test_todos.append(response.json()["id"])
        return response

    def cleanup(self):
        """Clean up any todos created during tests"""
        for todo_id in self.test_todos:
            requests.delete(f"{self.base_url}/todo/{todo_id}")
        self.test_todos = []

    def test_create_todo(self):
        response = self._create_todo()
        assert response.status_code == 200
        
        todo = response.json()
        assert todo["user_id"] == 1
        assert todo["text"] == "Test todo"
        assert "id" in todo
        assert "created_at" in todo
        assert "updated_at" in todo
        
        return todo["id"]

    def test_get_todos(self):
        # Create a few todos first
        self._create_todo(text="First todo")
        self._create_todo(text="Second todo")
        
        response = requests.get(f"{self.base_url}/todos")
        assert response.status_code == 200
        
        todos = response.json()
        assert isinstance(todos, list)
        assert len(todos) >= 2

    def test_get_single_todo(self):
        # Create a todo first
        response = self._create_todo()
        todo_id = response.json()["id"]
        
        # Get the created todo
        response = requests.get(f"{self.base_url}/todos/{todo_id}")
        assert response.status_code == 200
        
        todo = response.json()
        assert todo["id"] == todo_id
        
        # Test getting non-existent todo
        response = requests.get(f"{self.base_url}/todos/99999")
        assert response.status_code == 404

    def test_update_todo(self):
        # Create a todo first
        response = self._create_todo()
        todo_id = response.json()["id"]
        
        # Update the todo
        update_data = {"text": "Updated todo text"}
        response = requests.put(f"{self.base_url}/todo/{todo_id}", json=update_data)
        assert response.status_code == 200
        
        todo = response.json()
        assert todo["id"] == todo_id
        assert todo["text"] == update_data["text"]

    def test_delete_todo(self):
        # Create a todo first
        response = self._create_todo()
        todo_id = response.json()["id"]
        
        # Delete the todo
        response = requests.delete(f"{self.base_url}/todo/{todo_id}")
        assert response.status_code == 200
        self.test_todos.remove(todo_id)  # Remove from cleanup list
        
        # Verify todo is deleted
        response = requests.get(f"{self.base_url}/todos/{todo_id}")
        assert response.status_code == 404

    def test_invalid_data(self):
        # Test creating todo with missing fields
        response = requests.post(f"{self.base_url}/todo", json={"user_id": 1})
        assert response.status_code == 422
        
        response = requests.post(f"{self.base_url}/todo", json={"text": "Test"})
        assert response.status_code == 422

    def run_all_tests(self):
        """Run all test methods in the class"""
        test_methods = [method for method in dir(self) if method.startswith('test_')]
        
        for method in test_methods:
            try:
                print(f"Running {method}...")
                getattr(self, method)()
                print(f"✅ {method} passed")
            except AssertionError as e:
                print(f"❌ {method} failed: {str(e)}")
            except Exception as e:
                print(f"❌ {method} failed with error: {str(e)}")
            print("---")
            
        # Clean up after all tests
        self.cleanup()

if __name__ == "__main__":
    test_suite = TestTodoAPI()
    test_suite.run_all_tests()