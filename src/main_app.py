from fastapi import FastAPI, HTTPException, Request
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from js import Response, console
from pyodide.ffi import JsProxy

# Pydantic models
class TodoCreate(BaseModel):
    user_id: int
    text: str

class TodoUpdate(BaseModel):
    text: str

class Todo(BaseModel):
    id: int
    user_id: int
    text: str
    # created_at: datetime
    # updated_at: datetime

# Database operations class
class TodoDB:
    @staticmethod
    async def get_todos(db):
        query = """
            SELECT id, user_id, text
            FROM todos;
        """
        results = await db.prepare(query).all()
        return results.results

    @staticmethod
    async def get_todo(db, todo_id: int) -> Optional[dict]:
        query = """
            SELECT id, user_id, text, created_at, updated_at
            FROM todos
            WHERE id = ?;
        """
        results = await db.prepare(query).all(todo_id)
        return results.results[0] if results.results else None

    @staticmethod
    async def create_todo(db, todo: TodoCreate) -> dict:
        query = """
            INSERT INTO todos (user_id, text)
            VALUES (?, ?)
            RETURNING id, user_id, text, created_at, updated_at;
        """
        results = await db.prepare(query).all(todo.user_id, todo.text)
        return results.results[0]

    @staticmethod
    async def update_todo(db, todo_id: int, todo: TodoUpdate) -> Optional[dict]:
        query = """
            UPDATE todos
            SET text = ?
            WHERE id = ?
            RETURNING id, user_id, text, created_at, updated_at;
        """
        results = await db.prepare(query).all(todo.text, todo_id)
        return results.results[0] if results.results else None

    @staticmethod
    async def delete_todo(db, todo_id: int) -> bool:
        query = """
            DELETE FROM todos
            WHERE id = ?
            RETURNING id;
        """
        results = await db.prepare(query).all(todo_id)
        return len(results.results) > 0

# FastAPI app and endpoints
app = FastAPI()

@app.get("/todos")
async def get_todos(request: Request):
    results = await TodoDB.get_todos(request.scope["env"].DB)
    return results.to_py()

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int, request: Request):
    result = await TodoDB.get_todo(request.scope["env"].DB, todo_id)
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result

@app.post("/todo")
async def create_todo(todo: TodoCreate, request: Request):
    result = await TodoDB.create_todo(request.scope["env"].DB, todo)
    return result

@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate, request: Request):
    result = await TodoDB.update_todo(request.scope["env"].DB, todo_id, todo)
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, request: Request):
    success = await TodoDB.delete_todo(request.scope["env"].DB, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}