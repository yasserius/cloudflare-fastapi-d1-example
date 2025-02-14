# FastAPI Cloudflare Worker Example Todo List App with D1 Database Binding

## Warning: this app only works locally now, fastapi is experimental, deployment doesn't work yet

## Useful Links
- https://github.com/cloudflare/python-workers-examples
- https://developers.cloudflare.com/workers/languages/python/

## Guideline

You should have `npm` installed, I am using `10.9.0`. I am using WSL Ubuntu.

Then go on cloudflare and create a D1 database, get the `database_name` and `database_id` like described [here](https://developers.cloudflare.com/d1/get-started/) and put it into `wrangler.toml`:
```
name = "todos-fastapi-app"
main = "src/worker.py"
compatibility_flags = ["python_workers"]
compatibility_date = "2023-12-18"

[[d1_databases]]
binding = "DB"
database_name = "<name e.g. todos-db-1>"
database_id = "<code>"
```

Then run 
```
npx wrangler d1 execute todos-db-1 --local --file=./schema.sql
``` 
to populate the local database

You can check the local data using
```
npx wrangler d1 execute todos-db-1 --local --command="SELECT * FROM todos"
```

Finally run the local server:
```
npx wrangler@latest dev

```

You can go to `http://localhost:8787/todos` in your browser and you should see some results.

Feel free to report issues

## Common errors

### `ValueError: [TypeError("'pyodide.ffi.JsProxy' object is not iterable"), TypeError('vars() argument must have __dict__ attribute')]`

This happens because `pyodide.ffi.JsProxy` is not json serializable, so you have to use `.to_py()` to get native python object, like this:
```python
class TodoDB:
    @staticmethod
    async def get_todos(db):
        query = """
            SELECT id, user_id, text
            FROM todos;
        """
        results = await db.prepare(query).all()
        return results.results

@app.get("/todos")
async def get_todos(request: Request):
    results = await TodoDB.get_todos(request.scope["env"].DB)
    return results.to_py()
```