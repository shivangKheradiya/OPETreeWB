from .base import ElementSchema


class Site(ElementSchema):

    TYPE = "SITE"

    @classmethod
    def allowed_children(cls):
        return ["ZONE"]