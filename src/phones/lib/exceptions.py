from ninja.errors import ValidationError


def parse_pydantic_error(exception: ValidationError):
    msg = {}
    for error in exception.errors:
        match error["type"]:
            case "value_error":
                msg[error["loc"][2]] = error["msg"]

    return msg
