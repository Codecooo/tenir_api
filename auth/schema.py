from ninja import Schema


class RegisterIn(Schema):
    username: str
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""


class LoginIn(Schema):
    username: str
    password: str


class RegisterOut(Schema):
    message: str


class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_staff: bool