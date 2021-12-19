from fastapi import FastAPI,Form,File,UploadFile,responses
from pydantic import BaseModel
from deta import Deta,Drive

app = FastAPI(title = 'MadeLaugh')

@app.get('/')
async def home():
    return {'welcome to MadeLaugh'}

base = Deta()
photos = Drive('photos')

stories_base = base.Base('stories-crud')

@app.post('/upload_photo/',tags = ['photo'])
async def upload_photo(file : UploadFile = File(...)):
    return photos.put(file.filename,file.file)

@app.get('/get_photos_list/',tags = ['photo'])
async def get_photo_list():
    return photos.list()

@app.get("/stream/{name}",tags = ['photo'])
async def stream_file(name):
    imag = photos.get(name)
    extt = name.split(".")[1]
    return responses.StreamingResponse(imag.iter_chunks(),media_type =f"image/{extt}")

@app.delete('/delete_photo/{name}',tags = ['photo'])
async def delete(name : str):
    imag = photos.get(name)
    
    if imag:
        photos.delete(name)
        return {'photo deleted'}
    
    return {'photo not available to delete'}
    

class stories(BaseModel):
    title : str
    author : str
    category :str
    story : str


@app.post('/post_story/',tags = ['story'])
async def post_story(title : str = Form(...),author : str = Form(...),category : str = Form(...),story : str = Form(...)):
    story_show = stories_base.put({'TITLe':title,'AUTHOR':author,'CATEGORY':category,'STORY':story})
    return story_show
    
@app.get("/get_all_stories",tags = ['story'])
async def get_all():
    all_stories = stories_base.fetch()
    return all_stories

@app.get("/get_a_specific_story/{key}",tags = ['story'])
async def get_specific(key : str):
    specific = stories_base.get(key)
    
    if specific:
        return specific
    
    return {'story not found'}
    

@app.get('/get_category/{category}',tags = ['story'])
async def get_category(category : str):
    categories = stories_base.fetch({'CATEGORY':category})
    
    if categories:
        return categories
    
    return {'category not found'}


@app.delete('/delete_story/{key}',tags = ['story'])
async def deleting_a_story(key : str):
    specific = stories_base.get(key)
    
    if specific:
        stories_base.delete(key)
        return {'story deleted'}
    
    return {'story not available to delete'}

