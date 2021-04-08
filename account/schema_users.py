import graphene
from django.contrib.auth import  authenticate, get_user_model
from graphene import ObjectType
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username: str, password: str, email: str):
        user = get_user_model()(name=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(name=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    login = graphene.Field(UserType, username=graphene.String(), password=graphene.String())
    user = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_login(self, info, username, password, **kwargs):
        auth_user = authenticate(username=username, password=password)

        if auth_user == None:
            raise Exception("Credencial Invalida")
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
