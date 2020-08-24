import importlib
import inspect
import re
from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema as DefaultSwaggerAutoSchema
from drf_yasg.renderers import ReDocRenderer as BaseReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from inflection import camelize
from rest_framework import permissions
from rest_framework.exceptions import APIException

__all__ = ("RedocSchemaView", "SwaggerAutoSchema")

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


class SwaggerAutoSchema(DefaultSwaggerAutoSchema):
    def get_operation_id(self, operation_keys=None):
        operation_keys = operation_keys or self.operation_keys
        operation_id = self.overrides.get("operation_id", "")

        if not operation_id:
            if len(operation_keys) > 2:
                operation_keys = operation_keys[1:]

            # 복수형 처리 (notices, posts등을 notice, post로 변경)
            operation_keys = [
                key[:-1] if key[-1] == "s" else key for key in operation_keys
            ]
            # '-'처리 (auth-token을 AuthToken으로 처리)
            operation_keys = [key.replace("-", "_") for key in operation_keys]
            # PartialUpdate처리 (PartialUpdate -> Update로 출력)
            operation_keys = [
                key.replace("partial_update", "update") for key in operation_keys
            ]

            operation_id = " _".join(operation_keys)
        return camelize(operation_id)


class SchemaGenerator(OpenAPISchemaGenerator):
    PATTERN_ERASE_WORDS = re.compile(
        "|".join(["list", "create", "read", "update", "partial_update", "destroy"])
    )

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
