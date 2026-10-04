## hello gemini this is a test run review this code

from ninja import Router

from mountain.models import Mountain

router = Router()

@router.get("/hello")
def hello():
    mountain = Mountain.objects.first()
    return {"message": "Hello, World!", "mountain": mountain}