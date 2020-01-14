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


@policy_type.field("name")
def resolve_policy_name(obj, *_):
    return f'{obj.name}'


@policy_type.field("insured")
def resolve_insured(obj, *_):
    return {"uid": obj.insured}


@policy_type.field("accountManager")
def resolve_account_manager(obj, *_):
    return {"uid": obj.account_manager}


@policy_type.field("description")
def resolve_policy_description(obj, *_):
    return f'{obj.description}'


@query_type.field("policies")
def resolve_policies(_, info):
    try:
        policies = Policy.objects.all()
        return dict(
            policies=[policy for policy in policies]
            )
    except Exception as e:
        return dict(
            error=f"An error occurred: {e}"
        )


@mutation.field("createPolicy")
def resolve_create_policy(_, info, input):
    try:
        new_policy=Policy.objects.create(
            name=input["name"],
            insured=input["insured"],
            account_manager=input["accountManager"],
            description=input["description"]
        )

        return dict(
            policy=new_policy
        )
    except Exception as e:
        return dict(
            error=f"An error occurred {e}"
        )


manager.add_types(mutation, policy_type)

schema = manager.get_schema()