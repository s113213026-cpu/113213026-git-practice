# main.py
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from db import getDB,lifespan

#from routes import router as all_routes
#from routes.upload import router as upload_router
#from routes import users


templates = Jinja2Templates(directory="templates")
app = FastAPI(lifespan=lifespan)

from routes.r import router as myRoute

# Include the router
app.include_router(myRoute) #mount every thing from ./routes/ to url under prefix

@app.get("/")
async def index():
	return RedirectResponse(url="/students/list/template")

@app.get("/students/list")
async def read_users(db=Depends(getDB)):
	cur=await db.execute("SELECT * FROM students")
	return await cur.fetchall()

@app.get("/students/list/template")
async def stuList(request:Request, db=Depends(getDB)):
	cur=await db.execute("SELECT * FROM students order by stuid;")
	data= await cur.fetchall()
	return templates.TemplateResponse(name="studentList.html", request=request,context={"students": data})

@app.get("/student/edit/{stuid}")
async def stuEdit(stuid:int,request:Request, db=Depends(getDB)):
	cur=await db.execute("SELECT * FROM students where stuid=%s",(stuid,))
	data= await cur.fetchone()
	return templates.TemplateResponse(name="studentEdit.html", request=request,context={"data": data})


@app.get("/student/create")
async def stuCreatePage(request: Request):
	return templates.TemplateResponse(name="studentCreate.html", request=request)

@app.post("/student/create")
async def stuCreate(
	stuid: int = Form(...),
	name: str = Form(...),
	dept: str = Form("資管系"),
	height: int = Form(170),
	weight: int = Form(60),
	db = Depends(getDB)
):
	print(f"Creating student: {stuid}, {name}, {dept}, {height}, {weight}")
	await db.execute(
		"INSERT INTO students (stuid, name, dept, height, weight) VALUES (%s, %s, %s, %s, %s);",
		(stuid, name, dept, height, weight)
	)
	return RedirectResponse(url="/students/list/template", status_code=303)

@app.get("/student/delete/{stuid}")
@app.post("/student/delete/{stuid}")
async def stuDelete(stuid: int, db = Depends(getDB)):
	print(f"Deleting student: {stuid}")
	await db.execute("DELETE FROM students WHERE stuid = %s;", (stuid,))
	return RedirectResponse(url="/students/list/template", status_code=303)

@app.post("/student/update")
async def stuUpdate(
	stuid: int = Form(...),
	name: str = Form(...),
	height: int = Form(...),
	dept: str = Form(None),
	db = Depends(getDB)
):
	print(stuid, name, dept, height)
	if dept:
		await db.execute("UPDATE students SET name = %s, dept = %s, height = %s WHERE stuid = %s;", (name, dept, height, stuid))
	else:
		await db.execute("UPDATE students SET name = %s, height = %s WHERE stuid = %s;", (name, height, stuid))
	return RedirectResponse(url="/students/list/template", status_code=303) #use 303 to switch to GET

