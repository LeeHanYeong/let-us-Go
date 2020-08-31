import importlib
import inspect
import re
from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.renderers import ReDocRenderer as BaseReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.exceptions import APIException

__all__ = ("RedocSchemaView",)

from rest_framework.viewsets import ViewSetMixin

exceptions = []
drf_exceptions_module = importlib.import_module("utils.drf.exceptions")
for attr_name in dir(drf_exceptions_module):
    attr = getattr(drf_exceptions_module, attr_name)
    if (
        inspect.isclass(attr)
        and issubclass(attr, APIException)
        and attr is not APIException
    ):
        exceptions.append(attr)
DRF_EXCEPTION_CASES = [
    {
        "name": exc.__name__,
        "status": exc.status_code,
        "code": exc.default_code,
        "detail": exc.default_detail,
    }
    for exc in exceptions
]
DRF_EXCEPTION_DESCRIPTION = """
# Exceptions
{exceptions}
""".format(
    exceptions="\n\n".join(
        [
            "### {name}  \n"
            "status: {status}  \n"
            "code: `{code}`  \n"
            "detail: {detail}".format(
                name=exc["name"],
                status=exc["status"],
                code=exc["code"],
                detail=exc["detail"],
            )
            for exc in DRF_EXCEPTION_CASES
        ]
    )
)


class SchemaGenerator(OpenAPISchemaGenerator):
    DEFAULT_OPERATIONS = [
        "list",
        "create",
        "read",
        "update",
        "partial_update",
        "destroy",
    ]
    PATTERN_ERASE_WORDS = re.compile("|".join(DEFAULT_OPERATIONS))

    def get_operation_keys(self, subpath, method, view):
        keys = super().get_operation_keys(subpath, method, view)
        keys = [key.replace("partial_update", "update") for key in keys]
        return keys

    def get_operation(self, view, path, prefix, method, components, request):
        operation = super().get_operation(
            view, path, prefix, method, components, request
        )
        if operation is not None and "summary" not in operation:
            if issubclass(view.__class__, ViewSetMixin):
                action = view.action.replace("partial_update", "update").replace(
                    "-", "_"
                )
                keys = [item for item in [view.basename, *action.split("_")]]
            else:
                operation["operationId"] = operation["operationId"].replace("-", "_")
                if hasattr(view, "queryset") and view.queryset is not None:
                    app_label = view.queryset.model._meta.app_label
                    model_name = view.queryset.model.__name__
                    keys = [
                        model_name if model_name in item else item
                        for item in operation["operationId"].split("_")
                        if item != app_label
                    ]
                else:
                    keys = [item for item in operation["operationId"].split("_")]
            operation["summary"] = " ".join([key.capitalize() for key in keys])
        return operation

    def get_paths_object(self, paths: OrderedDict):
        # operation_id에서, PATTERN_ERASE_WORDS에 해당하는 단어를 지운 후 오름차순으로 정렬
        def path_sort_function(path_tuple):
            operation_id = path_tuple[1].operations[0][1]["operationId"]
            operation_id = self.PATTERN_ERASE_WORDS.sub("", operation_id)
            return operation_id

        paths = OrderedDict(sorted(paths.items(), key=path_sort_function))
        # 마지막에 /(slash)가 붙은 경우, 제거함
        paths = OrderedDict(
            {k[:-1] if k[-1] == "/" else k: v for k, v in paths.items()}
        )
        return super().get_paths_object(paths)


BaseSchemaView = get_schema_view(
    openapi.Info(
        title="let us: Go! API",
        default_version="v1",
        description="let us: Go! API Documentation\n" + DRF_EXCEPTION_DESCRIPTION,
        contact=openapi.Contact(email="dev@lhy.kr"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=SchemaGenerator,
)


class ReDocRenderer(BaseReDocRenderer):
    template = "docs/redoc.html"


class RedocSchemaView(BaseSchemaView):
    renderer_classes = (ReDocRenderer, OpenAPIRenderer)
