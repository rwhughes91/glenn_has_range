"""pluralized table names

Revision ID: 177457e2c2ad
Revises: 8ba1e8335ee1
Create Date: 2021-03-05 22:38:14.076915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "177457e2c2ad"
down_revision = "8ba1e8335ee1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "blacklist_tokens",
        sa.Column("token_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=500), nullable=False),
        sa.Column("blacklisted_on", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("token_id"),
        sa.UniqueConstraint("token"),
    )
    op.create_table(
        "playlists",
        sa.Column("playlist_id", sa.String(length=100), nullable=False),
        sa.Column("datasource", sa.String(), nullable=False),
        sa.Column("screen_name", sa.String(), nullable=False),
        sa.Column("playlist_link", sa.String(), nullable=False),
        sa.Column("playlist_description", sa.Text(), nullable=True),
        sa.Column("last_update", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.user_id"],
        ),
        sa.PrimaryKeyConstraint("playlist_id"),
        sa.UniqueConstraint("playlist_link"),
    )
    op.drop_table("playlist")
    op.drop_table("blacklist_token")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "blacklist_token",
        sa.Column("token_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("token", sa.VARCHAR(length=500), autoincrement=False, nullable=False),
        sa.Column(
            "blacklisted_on",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("token_id", name="blacklist_token_pkey"),
        sa.UniqueConstraint("token", name="blacklist_token_token_key"),
    )
    op.create_table(
        "playlist",
        sa.Column(
            "playlist_id", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
        sa.Column("datasource", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("screen_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("playlist_link", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "playlist_description", sa.TEXT(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "last_update", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("created_by", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by"], ["users.user_id"], name="playlist_created_by_fkey"
        ),
        sa.PrimaryKeyConstraint("playlist_id", name="playlist_pkey"),
        sa.UniqueConstraint("playlist_link", name="playlist_playlist_link_key"),
    )
    op.drop_table("playlists")
    op.drop_table("blacklist_tokens")
    # ### end Alembic commands ###
