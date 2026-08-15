from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Query, Path
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = [],
    metadata: Dict[str, str] = {"key": "value"}
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int=1):
    return {
        'id': id,
        'data': blog,
        'version': version
        }

@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, 
                   id: int, 
                   comment_title: int = Query(None,
                                           title='Title of the comment',
                                           description='description for comment_title',
                                           alias='commentTitle',
                                           deprecated=True
                                           ),
                    content: str = Body(..., # or can use Body(Ellipsis)
                                        min_length=10,
                                        max_length=50,
                                        pattern='^[a-z\s]*$'
                                        ),
                    comment_id: int = Path(gt=5, le=10),
                    v: Optional[List[str]] = Query(['1.0', '1.1', '1.2'])
                   ):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'content': content,
        'comment_id': comment_id,
        'version': v
    }

def required_functionality():
    return {'message': 'Learning FastAPI is important'}