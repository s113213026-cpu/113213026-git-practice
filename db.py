# db.py
import sys
import os
import asyncio

# On Windows, psycopg async requires SelectorEventLoop
if sys.platform == "win32":
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
	db_password = os.getenv("PGPASSWORD", "0000")
	app.state.pool = AsyncConnectionPool(
		conninfo = f"postgresql://postgres:{db_password}@localhost:5432/mydb",
		kwargs={"row_factory": dict_row},
		open=False,
		#min_size=1,
		#max_size=10,
		#timeout=10,
		)
	await app.state.pool.open()
	print("[OK] Connected to DB")

	yield  # App runs here

	# Shutdown logic
	await app.state.pool.close()
	print("[STOP] Disconnected from DB")

#a wrapper for fastAPI's Depends Injection
async def getDB(request: Request):
	async with request.app.state.pool.connection() as conn:
		#set cuurent login user from session
		yield conn
