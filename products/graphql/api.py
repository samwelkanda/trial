from os.path import dirname, join
from ariadne import QueryType, MutationType, ScalarType, UnionType, ObjectType
from ariadne import gql, make_executable_schema, snake_case_fallback_resolvers, upload_scalar
from ariadne import load_schema_from_path, gql
from ariadne.contrib.django.scalars import date_scalar, datetime_scalar

from ariadne_extensions import federation

from products.policies.models import Policy

type_def = load_schema_from_path("./products/graphql/schema.graphql")
type_defs = gql(type_def)

query_type = QueryType()
mutation = MutationType()
policy_type = ObjectType('Policy')


manager = federation.FederatedManager(
    schema_sdl_file=join(dirname(__file__), 'schema.graphql'),
    query=query_type,
)

@query_type.field("policies")
def resolve_policies(_, info):
    try:
        policies = Policy.objects.all()
        return dict(
            policies=[policy.serialize() for policy in policies]
            )
    except Exception as e:
        return dict(
            error=f"An error occurred: {e}"
        )

# @query_type.field("policy")
# def resolve_policy(_, info, uid):
#     policy = Policy.objects.get(uid=uid)
#     return dict(policy=policy.serialize())

@mutation.field("createPolicy")
def resolve_create_policy(_, info, input):
    try:
        new_policy=Policy.objects.create(
            name=input["name"],
            insured=input["insured"],
            description=input["description"]
        )

        return dict(
            policy=new_policy.serialize()
        )
    except Exception as e:
        return dict(
            error=f"An error occurred {e}"
        )


manager.add_types(mutation, policy_type)

schema = manager.get_schema()