import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ..models import Playlist, User, BlacklistToken
from ..services import get_playlists
from .utils import get_col_name_from_enum


class PlaylistType(SQLAlchemyObjectType):
    """Graphql Type for Playlist model"""

    class Meta:
        model = Playlist
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, playlist_id: str) -> Playlist:
        """Fetch playlist node"""

        return Playlist.query.filter_by(playlist_id=playlist_id).first()


class UserType(SQLAlchemyObjectType):
    """Graphql Type for User model"""

    class Meta:
        model = User
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, public_id: str) -> User:
        """Fetch user node"""

        return User.query.filter_by(public_id=public_id).first()


class BlacklistTokenType(SQLAlchemyObjectType):
    """Graphql Type for BlacklistToken Model"""

    class Meta:
        model = BlacklistToken
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, token_id: str) -> BlacklistToken:
        """Fetch token node"""

        return BlacklistToken.query.filter_by(token_id=token_id)


class Query(graphene.ObjectType):
    """Query Root for schema"""

    node = relay.Node.Field()
    all_playlists = SQLAlchemyConnectionField(
        PlaylistType.connection,
        datasource=graphene.String(),
        screen_name=graphene.String(),
        playlist_link=graphene.String(),
        playlist_description=graphene.String(),
    )
    all_users = SQLAlchemyConnectionField(UserType.connection)
    all_tokens = SQLAlchemyConnectionField(BlacklistTokenType.connection)

    def resolve_all_playlists(self, info, **kwargs):
        """All playlists query"""

        sort_by = kwargs.get("sort", [])

        filters_keys = [
            "datasource",
            "screen_name",
            "playlist_link",
            "playlist_description",
        ]
        filters = {
            key: kwargs.get(key) for key in filters_keys if kwargs.get(key) is not None
        }

        return get_playlists(
            filters=filters, order_by=get_col_name_from_enum(sort_by)[0]
        )


schema = graphene.Schema(query=Query)
