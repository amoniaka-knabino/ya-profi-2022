user_already_exists_message = (
    "Данный пользователь уже зарегистрирован в базе данных"
)

user_not_found_message = (
    "Данный пользователь не найден в базе данных"
)


def get_error_json_dict(err_message):
    return {
        "error": err_message
    }
