import json
from typing import IO, Any, Dict, List, Optional, Tuple

from django.http import HttpResponse
from django.test import Client, TestCase


class BaseGraphQLQueryTest(TestCase):
    @staticmethod
    def get_client():
        return Client()

    @classmethod
    def get_operations(
        cls,
        query: str,
        variables: Optional[Dict] = None,
        operation_name: Optional[str] = None,
        input_data: Optional[Dict] = None,
    ) -> Dict:
        if variables is None:
            variables = {}

        if input_data:
            variables["input"] = input_data

        operations = {
            "query": query,
            "variables": variables,
        }
        if operation_name:
            operations["operationName"] = operation_name

        return operations

    @classmethod
    def get_file_map_data(cls, files: List[IO]) -> Tuple[Dict, Dict]:
        file_map = {}
        map_data = {}
        for count, file in enumerate(files):
            map_data[f"{count}"] = ["variables.file"]
            file_map[count] = file

        return map_data, file_map

    @classmethod
    def query(
        cls,
        query: str,
        client: Optional[Client] = None,
        operation_name: Optional[str] = None,
        input_data: Optional[Dict] = None,
        variables: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        files: Optional[List[IO]] = None,
        url: str = "/graphql/",
    ) -> HttpResponse:
        if client is None:
            client = cls.get_client()

        if headers is None:
            headers = {}

        if files is None:
            files = []

        arguments: Dict[str, Any] = {}
        operations_data = cls.get_operations(query, variables, operation_name, input_data)
        if files:
            operations_data["variables"]["file"] = None
            map_data, file_map = cls.get_file_map_data(files)

            data: Any = {"operations": json.dumps(operations_data), "map": json.dumps(map_data), **file_map}
            arguments["format"] = "multipart"
        else:
            data = json.dumps(operations_data)
            arguments["format"] = "json"
            arguments["content_type"] = "application/json"

        rsp = client.post(url, data, **headers, **arguments)
        return rsp
