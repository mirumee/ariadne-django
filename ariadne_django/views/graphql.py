from typing import cast

from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ariadne.exceptions import HttpBadRequestError
from ariadne.graphql import graphql_sync

from graphql import GraphQLSchema

from .base import BaseGraphQLView


@method_decorator(csrf_exempt, name="dispatch")
class GraphQLView(BaseGraphQLView):
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
