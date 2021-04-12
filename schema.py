import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database import User, Store, db_session
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_header_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required
)


class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )


class StoreObject(SQLAlchemyObjectType):
    class Meta:
        model = Store
        interfaces = (graphene.relay.Node,)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserObject)
    
    class Arguments:
        username =graphene.String(required=True)
        password =graphene.String(required=True)
        email =graphene.String(required=True)
    
    def mutate(self, info, username, password , email):
        user = User.query.filter_by(username=username).first()
        if user:
            return CreateUser(user=user)
        user = User(username=username,password=password,email=email)
        if user:
            db_session.add(user)
            db_session.commit()
        return CreateUser(user=user)


class ProtectedStore(graphene.Union):
    class Meta:
        types = (StoreObject,AuthInfoField)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    
    all_users = SQLAlchemyConnectionField(UserObject)
    all_stores = SQLAlchemyConnectionField(StoreObject)
    get_store = graphene.Field(type=ProtectedStore, token=graphene.String(),id=graphene.Int())

    # pass access token into the header of the request:
    @query_header_jwt_required
    def resolve_get_store(self,info,id):
        store_qry = StoreObject.get_query(info)
        storeval = store_qry.filter(Store.id.contains(id)).first()
        return storeval

    # def resolve_all_users(self, info, filters=None):
    #     query = User.query
    #     if filters is not None:
    #         query = UserFilter.filter(info, query, filters)

    #     return query        


class AuthMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String()
        password = graphene.String()
    
    def mutate(self, info , username, password) :
        user = User.query.filter_by(username=username).first()
        print(user)
        if not user:
            raise Exception('Authenication Failure : User is not registered')
        return AuthMutation(
            access_token = create_access_token(username),
            refresh_token = create_refresh_token(username)
        )


class CreateStore(graphene.Mutation):
    store = graphene.Field(ProtectedStore)

    class Arguments:
        name = graphene.String(required=True)
        user_id = graphene.Int(required=True)
        token = graphene.String()

    @mutation_jwt_required
    def mutate(self, info, name, user_id):
        store = Store(name=name, user_id=user_id)
        if store:
            db_session.add(store)
            db_session.commit()
        return CreateStore(store=store)


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @mutation_jwt_refresh_token_required
    def mutate(self):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    auth = AuthMutation.Field()
    protected_create_store = CreateStore.Field()
    refresh = RefreshMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)