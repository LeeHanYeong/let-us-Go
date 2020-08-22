from typing import Sequence, Tuple

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

__all__ = ("schema",)


def schema(view, methods: Sequence[Tuple[str, dict]]):
    for method in methods:
        name = method[0]
        if name == "update":
            name = "partial_update"
        view = method_decorator(name=name, decorator=swagger_auto_schema(**method[1]))(
            view
        )
    return view
