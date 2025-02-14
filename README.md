npx wrangler@latest dev

npx wrangler d1 execute todos-db-1 --local --file=./schema.sql

npx wrangler d1 execute todos-db-1 --local --command="SELECT * FROM todos"