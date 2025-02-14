from fastapi import FastAPI, HTTPException, Request
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

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
    created_at: datetime
    updated_at: datetime

# Database operations class
class TodoDB:
    @staticmethod
    async def get_todos(db):
        query = """
            SELECT id, user_id, text, created_at, updated_at
            FROM todos
            ORDER BY created_at DESC;
        """
        results = await db.prepare(query).all()
        return results.results

    @staticmethod
    async def get_todo(db, todo_id: int):
        query = f"""
            SELECT id, user_id, text, created_at, updated_at
            FROM todos
            WHERE id = {todo_id};
        """
        results = await db.prepare(query).all()
        return results.results[0] if results.results else None

    @staticmethod
    async def create_todo(db, todo: TodoCreate):
        query = f"""
            INSERT INTO todos (user_id, text)
            VALUES ({todo.user_id}, '{todo.text}')
            RETURNING id, user_id, text, created_at, updated_at;
        """
        results = await db.prepare(query).all()
        return results.results[0]

    @staticmethod
    async def update_todo(db, todo_id: int, todo: TodoUpdate):
        query = f"""
            UPDATE todos
            SET text = '{todo.text}'
            WHERE id = {todo_id}
            RETURNING id, user_id, text, created_at, updated_at;
        """
        results = await db.prepare(query).all()
        return results.results[0] if results.results else None

    @staticmethod
    async def delete_todo(db, todo_id: int):
        query = f"""
            DELETE FROM todos
            WHERE id = {todo_id}
            RETURNING id;
        """
        results = await db.prepare(query).all()
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
    return result.to_py()

@app.post("/todo")
async def create_todo(todo: TodoCreate, request: Request):
    result = await TodoDB.create_todo(request.scope["env"].DB, todo)
    return result.to_py()

@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate, request: Request):
    result = await TodoDB.update_todo(request.scope["env"].DB, todo_id, todo)
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result.to_py()

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, request: Request):
    success = await TodoDB.delete_todo(request.scope["env"].DB, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}