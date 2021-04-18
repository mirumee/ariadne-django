import asyncio
from typing import cast

from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.csrf import csrf_exempt

from ariadne.exceptions import HttpBadRequestError
from ariadne.graphql import graphql

from graphql import GraphQLSchema

from .base import BaseGraphQLView


@method_decorator(csrf_exempt, name="dispatch")
class GraphQLAsyncView(BaseGraphQLView):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine  # pylint: disable=protected-access
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
