from ariadne_django.views import GraphQLView


def test_playground_html_is_served_on_get_request(request_factory, snapshot, schema):
    view = GraphQLView.as_view(schema=schema)
    response = view(request_factory.get("/graphql/"))
    assert response.status_code == 200
    snapshot.assert_match(response.content)


def test_playground_options_can_be_set_on_view_init(request_factory, snapshot, schema):
    view = GraphQLView.as_view(schema=schema, playground_options={"test.option": True})
    response = view(request_factory.get("/graphql/"))
    assert response.status_code == 200
    snapshot.assert_match(response.content)
