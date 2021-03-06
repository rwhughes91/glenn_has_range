import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ..models import Playlist, User, BlacklistToken


class PlaylistType(SQLAlchemyObjectType):
    """Graphql Type for Playlist model"""

    class Meta:
        model = Playlist
        interfaces = (relay.Node,)


class UserType(SQLAlchemyObjectType):
    """Graphql Type for User model"""

    class Meta:
        model = User
        interfaces = (relay.Node,)


class BlacklistTokenType(SQLAlchemyObjectType):
    """Graphql Type for BlacklistToken Model"""

    class Meta:
        model = BlacklistToken
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    """Query Root for schema"""

    node = relay.Node.Field()
    all_playlists = SQLAlchemyConnectionField(PlaylistType.connection)
    all_users = SQLAlchemyConnectionField(UserType.connection)
    all_tokens = SQLAlchemyConnectionField(BlacklistTokenType.connection)


schema = graphene.Schema(query=Query)
