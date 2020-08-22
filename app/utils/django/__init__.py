from django.db.models import (
    QuerySet as DjangoQuerySet,
    Manager as DjangoManager,
    When,
    Value,
    Case,
)

__all__ = (
    "QuerySet",
    "Manager",
)


class QuerySet(DjangoQuerySet):
    def annotate_choices(self, output_dict=None):
        """
        choices가 존재하는 필드들의 get_FOO_display() 값을 annotate처리
        output_dict에 field.name을 사용해 별도의 output_field를 지정할 수 있다
        :param output_dict: {field.name: Field()}
        :return: QuerySet instance
        """
        annotate_dict = {}
        for field in self.model._meta.fields:
            if field.choices:
                case_args = [
                    When(**{field.name: k, "then": Value(v)})
                    for k, v in field.flatchoices
                ]
                case_kwargs = {"output_field": field.__class__()}
                if output_dict and field.name in output_dict:
                    case_kwargs["output_field"] = output_dict[field.name]
                annotate_dict[f"{field.name}_display"] = Case(
                    *case_args, **case_kwargs,
                )
        return self.annotate(**annotate_dict)


class Manager(DjangoManager.from_queryset(QuerySet)):
    pass
