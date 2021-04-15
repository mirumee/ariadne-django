import asyncio
import json
from typing import Any, Callable, Optional, Union, cast

from django.conf import settings
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from ariadne.constants import DATA_TYPE_JSON, DATA_TYPE_MULTIPART
from ariadne.exceptions import HttpBadRequestError
from ariadne.file_uploads import combine_multipart_data
from ariadne.format_error import format_error
from ariadne.graphql import graphql, graphql_sync
from ariadne.types import ContextValue, ErrorFormatter, ExtensionList, RootValue, ValidationRules

from graphql import GraphQLSchema
from graphql.execution import MiddlewareManager


Extensions = Union[Callable[[Any, Optional[ContextValue]], ExtensionList], ExtensionList]

DEFAULT_PLAYGROUND_OPTIONS = {"request.credentials": "same-origin"}


class BaseView(TemplateView):
    http_method_names = ["get", "post", "options"]
    template_name = "ariadne_django/graphql_playground.html"
    playground_options: Optional[dict] = None
    introspection: bool = True
    schema: Optional[GraphQLSchema] = None
    context_value: Optional[ContextValue] = None
    root_value: Optional[RootValue] = None
    logger = None
    validation_rules: Optional[ValidationRules] = None
    error_formatter: Optional[ErrorFormatter] = None
    extensions: Optional[Extensions] = None
    middleware: Optional[MiddlewareManager] = None

    def _get(self, request: HttpRequest, *args, **kwargs):  # pylint: disable=unused-argument
        options = DEFAULT_PLAYGROUND_OPTIONS.copy()
        if self.playground_options:
            options.update(self.playground_options)

        return render(
            request,
            self.get_template_names(),
            {"playground_options": json.dumps(options)},
        )

    def extract_data_from_request(self, request: HttpRequest):
        content_type = request.content_type or ""
        content_type = content_type.split(";")[0]

        if content_type == DATA_TYPE_JSON:
            return self.extract_data_from_json_request(request)
        if content_type == DATA_TYPE_MULTIPART:
            return self.extract_data_from_multipart_request(request)

        raise HttpBadRequestError("Posted content must be of type {} or {}".format(DATA_TYPE_JSON, DATA_TYPE_MULTIPART))

    def extract_data_from_json_request(self, request: HttpRequest):
        try:
            return json.loads(request.body)
        except (TypeError, ValueError) as ex:
            raise HttpBadRequestError("Request body is not a valid JSON") from ex

    def extract_data_from_multipart_request(self, request: HttpRequest):
        try:
            operations = json.loads(request.POST.get("operations", "{}"))
        except (TypeError, ValueError) as ex:
            raise HttpBadRequestError("Request 'operations' multipart field is not a valid JSON") from ex
        try:
            files_map = json.loads(request.POST.get("map", "{}"))
        except (TypeError, ValueError) as ex:
            raise HttpBadRequestError("Request 'map' multipart field is not a valid JSON") from ex

        return combine_multipart_data(operations, files_map, request.FILES)

    def get_kwargs_graphql(self, request: HttpRequest) -> dict:
        context_value = self.get_context_for_request(request)
        extensions = self.get_extensions_for_request(request, context_value)

        return {
            "context_value": context_value,
            "root_value": self.root_value,
            "validation_rules": self.validation_rules,
            "debug": settings.DEBUG,
            "introspection": self.introspection,
            "logger": self.logger,
            "error_formatter": self.error_formatter or format_error,
            "extensions": extensions,
            "middleware": self.middleware,
        }

    def get_context_for_request(self, request: HttpRequest) -> Optional[ContextValue]:
        if callable(self.context_value):
            return self.context_value(request)  # pylint: disable=not-callable
        return self.context_value or {"request": request}

    def get_extensions_for_request(self, request: HttpRequest, context: Optional[ContextValue]) -> ExtensionList:
        if callable(self.extensions):
            return self.extensions(request, context)  # pylint: disable=not-callable
        return self.extensions


@method_decorator(csrf_exempt, name="dispatch")
class GraphQLView(BaseView):
    def dispatch(self, *args, **kwargs):
        if not self.schema:
            raise ValueError("GraphQLView was initialized without schema.")
        try:
            return super().dispatch(*args, **kwargs)
        except HttpBadRequestError as error:
            return HttpResponseBadRequest(error.message)

    def get(self, *args, **kwargs):
        return self._get(*args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):  # pylint: disable=unused-argument
        try:
            data = self.extract_data_from_request(request)
        except HttpBadRequestError as error:
            return HttpResponseBadRequest(error.message)
        success, result = graphql_sync(cast(GraphQLSchema, self.schema), data, **self.get_kwargs_graphql(request))
        status_code = 200 if success else 400
        return JsonResponse(result, status=status_code)


class GraphQLAsyncView(BaseView):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine  # pylint: disable=protected-access
        view.csrf_exempt = True
        return view

    async def get(self, *args, **kwargs):
        return self._get(*args, **kwargs)

    async def post(self, request: HttpRequest, *args, **kwargs):  # pylint: disable=unused-argument
        try:
            data = self.extract_data_from_request(request)
        except HttpBadRequestError as error:
            return HttpResponseBadRequest(error.message)
        success, result = await graphql(cast(GraphQLSchema, self.schema), data, **self.get_kwargs_graphql(request))
        status_code = 200 if success else 400
        return JsonResponse(result, status=status_code)
