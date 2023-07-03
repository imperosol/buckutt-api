from ninja_extra.exceptions import APIException


class BadCartException(APIException):
    status_code = 404
    detail = "Some articles don't exist"
    # bad_articles = [1, 2, 3]

    # def __init__(self, bad_articles: list[int]):
    #     self.bad_articles = bad_articles
