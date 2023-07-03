from ninja_extra.exceptions import APIException


class NotEnoughCredit(APIException):
    status_code = 402
    detail = "Not enough credit"
