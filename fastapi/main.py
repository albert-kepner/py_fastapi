from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel

class Shape(BaseModel):
    name: str
    sides: int
    id: int

app = FastAPI()

client = MongitaClientDisk()
db = client.db
shapes = db.shapes
print(f'{shapes=}')
# shapes.insert_one({"id": 1, "name": "circle", "sides": 0})
# shapes.insert_one({"id": 2, "name": "triangle", "sides": 3})
# shapes.insert_one({"id": 3, "name": "square", "sides": 4})
# shapes.insert_one({"id": 4, "name": "pentagon", "sides": 5})
# shapes.insert_one({"id": 5, "name": "hexagon", "sides": 6})
# shapes.insert_one({"id": 6, "name": "heptagon", "sides": 7})
# shapes.insert_one({"id": 7, "name": "octagon", "sides": 8}) 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shapes")
async def get_shapes():
    existing_shapes = shapes.find({})
    return [
       {key:shape[key] for key in shape if key != "_id"}
       for shape in existing_shapes 
    ]

@app.get("/shapes/{shape_id}")
async def get_shape_by_id(shape_id: int):
    if shapes.count_documents({"id": shape_id}) > 0:
        shape = shapes.find_one({"id": shape_id})
        return {key:shape[key] for key in shape if key != "_id"} 
    raise HTTPException(status_code=404, detail=f'No shape with id {shape_id} found')

@app.post("/shapes")
async def post_shape(shape: Shape):
    shapes.insert_one(shape.model_dump())
    return shape

@app.put("/shapes/{shape_id}")
async def update_shape(shape_id: int, shape: Shape):
    if shapes.count_documents({"id": shape_id}) > 0:
        shapes.replace_one({"id": shape_id}, shape.model_dump())
        return shape
    raise HTTPException(status_code=404, detail=f'No shape with id {shape_id} found')
    
    