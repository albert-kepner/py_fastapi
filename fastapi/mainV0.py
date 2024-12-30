from fastapi import FastAPI, HTTPException

app = FastAPI()

shapes = [
    {"item_name": "Circle", "no_of_sides": 1, "id": 1},
    {"item_name": "Triangle", "no_of_sides": 3, "id": 2},
    {"item_name": "Octogon", "no_of_sides": 8, "id": 3},
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shapes")
async def get_shapes():
    return shapes

@app.get("/shapes/{shape_id}")
async def get_shape_by_id(shape_id: int):
    for shape in shapes:
        if shape["id"] == shape_id:
            return shape
    raise HTTPException(status_code=404, detail=f'No shape with id {shape_id} found')