import io
from unittest import mock

from django.test import Client

from ariadne_django.tests.graphql_query_test import BaseGraphQLQueryTest


def test_get_client():
    client = BaseGraphQLQueryTest.get_client()
    assert isinstance(client, Client)


def test_get_operations_with_all_options():
    operations = BaseGraphQLQueryTest.get_operations(
        "cat says meow",
        variables={"duck": "quack"},
        operation_name="dog",
        input_data={"height": "1m", "weight": "31kg"},
    )
    assert operations == {
        "query": "cat says meow",
        "variables": {"input": {"height": "1m", "weight": "31kg"}, "duck": "quack"},
        "operationName": "dog",
    }


def test_get_operations_without_operation_name():
    operations = BaseGraphQLQueryTest.get_operations(
        "cat says meow",
        variables={"duck": "quack"},
        input_data={"height": "1m", "weight": "31kg"},
    )
    assert operations == {
        "query": "cat says meow",
        "variables": {"input": {"height": "1m", "weight": "31kg"}, "duck": "quack"},
    }


def test_get_operations_without_input_data():
    operations = BaseGraphQLQueryTest.get_operations(
        "cat says meow",
        variables={"duck": "quack"},
        operation_name="dog",
    )
    assert operations == {
        "query": "cat says meow",
        "variables": {"duck": "quack"},
        "operationName": "dog",
    }


def test_get_operations_without_variables():
    operations = BaseGraphQLQueryTest.get_operations(
        "cat says meow",
        operation_name="dog",
        input_data={"height": "1m", "weight": "31kg"},
    )
    assert operations == {
        "query": "cat says meow",
        "variables": {"input": {"height": "1m", "weight": "31kg"}},
        "operationName": "dog",
    }


def test_get_file_map_data():
    test_file = io.StringIO("a file")
    map_data, file_map = BaseGraphQLQueryTest.get_file_map_data([test_file])
    assert map_data == {"0": ["variables.file"]}
    assert file_map == {0: test_file}


def test_json_query_happy_path():
    with mock.patch("django.test.client.Client.post") as mocked_fxn:
        client = Client()
        BaseGraphQLQueryTest.query(
            "meow",
            client,
            operation_name="dog",
            input_data={"height": "1m", "weight": "31kg"},
            variables={"duck": "quack"},
            headers={"APITOKEN": "OldMcDonald"},
            files=None,
            url="/baabaa",
        )
        mocked_fxn.assert_called_once_with(
            "/baabaa",
            '{"query": "meow", "variables": {"duck": "quack", "input": {"height": "1m", "weight": "31kg"}}, "operationName": "dog"}',  # pylint: disable=line-too-long
            APITOKEN="OldMcDonald",
            format="json",
            content_type="application/json",
        )


def test_multipart_query_happy_path():
    with mock.patch("django.test.client.Client.post") as mocked_fxn:
        client = Client()
        test_file = io.StringIO("a file")
        BaseGraphQLQueryTest.query(
            "meow",
            client,
            operation_name="dog",
            input_data={"height": "1m", "weight": "31kg"},
            variables={"duck": "quack"},
            headers={"APITOKEN": "OldMcDonald"},
            files=[test_file],
            url="/baabaa",
        )
        mocked_fxn.assert_called_once_with(
            "/baabaa",
            {
                "operations": '{"query": "meow", "variables": {"duck": "quack", "input": {"height": "1m", "weight": "31kg"}, "file": null}, "operationName": "dog"}',  # pylint: disable=line-too-long
                "map": '{"0": ["variables.file"]}',
                0: test_file,
            },
            APITOKEN="OldMcDonald",
            format="multipart",
        )


def test_query_without_client():
    with mock.patch("ariadne_django.tests.graphql_query_test.BaseGraphQLQueryTest.get_client") as mocked_fxn:
        BaseGraphQLQueryTest.query(
            "meow",
        )
        assert mocked_fxn.call_count == 1
