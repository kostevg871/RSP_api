from fastapi import HTTPException


def containt_only_letters():
    raise HTTPException(status_code=400, detail={
        "code": 2.1,
        "type": "ContaintOnlyLetters",
        "error_info": "Имя пользователя может содержать только буквы",
        "msg_user_ru": "Поле ИМЯ может содержать только буквы",
        "msg_user_en": "Name should contains only letters",
        "request_info": None
    })


def user_email_already_exist():
    raise HTTPException(status_code=400, detail={
        "code": 2.2,
        "type": "UserEmailAlreadyExist",
        "error_info": "Пользователь с такой почтой уже существует",
        "msg_user_ru": "Пользователь уже существует",
        "msg_user_en": "The user already exists",
        "request_info": None
    })


def email_incorrect():
    raise HTTPException(status_code=400, detail={
        "code": 2.3,
        "type": "EmailIncorrect",
        "error_info": "Некорректный e-mail",
        "msg_user_ru": "Неправильно введен e-mail",
        "msg_user_en": "Incorrect email entered",
        "request_info": None
    })
