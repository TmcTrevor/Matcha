"""create db tables

Revision ID: e629d9ca0c9a
Revises:
Create Date: 2025-11-18 12:02:49.498499

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e629d9ca0c9a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ENUM_NAME = 'gender'
ENUM_VALUES = ['female', 'male']
SEXUAL_PREF_VALUES = ['heterosexual', 'homosexual', 'bisexual']


def upgrade() -> None:
    """Upgrade schema."""

    # create types
    op.execute(f"""
               CREATE TYPE {ENUM_NAME} AS ENUM({', '.join(f"'{s}'" for s in ENUM_VALUES)});
            """)
    op.execute(f"""
               CREATE TYPE preference AS ENUM({', '.join(f"'{s}'" for s in SEXUAL_PREF_VALUES)});
               """)
    # create User Table
    op.execute("""
               CREATE TABLE IF NOT EXISTS users (
                   user_id SERIAL PRIMARY KEY,
                   email VARCHAR(50) NOT NULL,
                   password VARCHAR(50) NOT NULL,
                   username VARCHAR(50) NOT NULL,
                   first_name TEXT,
                   last_name TEXT,
                   gender GENDER,
                   sexual_pref PREFERENCE DEFAULT 'bisexual',
                   bio TEXT,
                   interests TEXT [],
                   city TEXT,
                   country TEXT,
                   phone_number TEXT,
                   two_factor_auth BOOLEAN DEFAULT FALSE,
                   fame_rate INT NOT NULL DEFAULT 0,
                   created_at TIMESTAMP,
                   UNIQUE (email, username)
               );
               """)
    # create image table
    op.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id SERIAL PRIMARY KEY,
            image_url TEXT NOT NULL,
            is_main BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP
        )
               """)
    # create PHOTO LIKE table
    op.execute("""
               CREATE TABLE IF NOT EXISTS image_likes (
                   image_like SERIAL PRIMARY KEY,
                   user_id INT,
                   image_id INT,
                   created_at TIMESTAMP,
                   CONSTRAINT fk_user_id
                   FOREIGN KEY (user_id)
                   REFERENCES users(user_id),
                   CONSTRAINT fk_image_id
                   FOREIGN KEY (image_id)
                   REFERENCES images(image_id)
               )
               """)
    # create visit table
    op.execute("""
               CREATE TABLE IF NOT EXISTS visits (
                   visit_id SERIAL PRIMARY KEY,
                   visitor_id INT,
                   visited_id INT,
                   visited_at TIMESTAMP,
                   is_hidden BOOLEAN,
                   created_at TIMESTAMP,
                   CONSTRAINT fk_visitor_id
                   FOREIGN KEY (visitor_id)
                   REFERENCES users(user_id),
                   CONSTRAINT fk_visited_id
                   FOREIGN KEY (visited_id)
                   REFERENCES users(user_id)
               )
               """)
    # create like table
    op.execute("""
               CREATE TABLE IF NOT EXISTS likes (
                   like_id SERIAL PRIMARY KEY,
                   liker_id INT,
                   target_id INT,
                   created_at TIMESTAMP,
                   CONSTRAINT fk_liker_id
                    FOREIGN KEY (liker_id)
                    REFERENCES users(user_id),
                    CONSTRAINT fk_target_id
                    FOREIGN KEY (target_id)
                    REFERENCES users(user_id)
               )
               """)
    # create match table
    op.execute("""
               CREATE TABLE IF NOT EXISTS matches (
                   match_id SERIAL PRIMARY KEY,
                   user1_id INT,
                   user2_id INT,
                   matched_at TIMESTAMP,
                   is_match_active BOOLEAN DEFAULT FALSE,
                   created_at TIMESTAMP,
                   CONSTRAINT fk_first_match_id
                    FOREIGN KEY (user1_id)
                    REFERENCES users(user_id),
                    CONSTRAINT fk_second_match_id
                    FOREIGN KEY (user2_id)
                    REFERENCES users(user_id)
               )
               """)
    # create conversation table
    op.execute("""
               CREATE TABLE IF NOT EXISTS conversations (
                   conversation_id SERIAL PRIMARY KEY,
                   first_member_id INT,
                   second_member_id INT,
                   is_active BOOLEAN,
                   last_message_id INT,
                   last_message_at TIMESTAMP,
                   last_read_msg_user1_id INT,
                   last_read_msg_user2_id INT,
                   last_read_msg_user1_at TIMESTAMP,
                   last_read_msg_user2_at TIMESTAMP,
                   created_at TIMESTAMP,
                   CONSTRAINT fk_first_member_id
                   FOREIGN KEY (first_member_id)
                   REFERENCES users(user_id),
                   CONSTRAINT fk_second_member_id
                   FOREIGN KEY (second_member_id)
                   REFERENCES users(user_id)
               )
               """)
    # create message table
    op.execute("""
               CREATE TABLE IF NOT EXISTS messages (
                   message_id SERIAL PRIMARY KEY,
                   conversation_id INT,
                   sender_id INT,
                   content_type VARCHAR(100),
                   content TEXT,
                   metadata JSONB,
                   is_system BOOLEAN,
                   created_at TIMESTAMP,
                   deleted_at TIMESTAMP,
                   edited_at TIMESTAMP,
                   CONSTRAINT fk_sender_id
                   FOREIGN KEY (sender_id)
                   REFERENCES users(user_id)
               )
               """)
    # update messages table
    op.execute("""
               ALTER TABLE messages
               ADD CONSTRAINT fk_conversation_id
                   FOREIGN KEY (conversation_id)
                   REFERENCES conversations(conversation_id)
               """)
    # # update conversations table
    op.execute("""
               ALTER TABLE conversations
               ADD CONSTRAINT fk_last_message_id
               FOREIGN KEY (last_message_id)
               REFERENCES messages(message_id),
               ADD CONSTRAINT fk_last_read_message_by_user1_id
                FOREIGN KEY (last_read_msg_user1_id)
                REFERENCES messages(message_id),
                ADD CONSTRAINT fk_last_read_message_by_user2_id
                FOREIGN KEY (last_read_msg_user2_id)
                REFERENCES messages(message_id)
               """)
    # create notification table
    op.execute("""
               CREATE TABLE IF NOT EXISTS notifications (
                   notification_id SERIAL PRIMARY KEY,
                   user_id INT,
                   type VARCHAR(250),
                   actor_user_id INT,
                   payload JSONB,
                   is_read BOOLEAN,
                   created_at TIMESTAMP,
                   CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(user_id),
                   CONSTRAINT fk_actor_user_id FOREIGN KEY (actor_user_id) REFERENCES users(user_id)
               )
               """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE users")
    op.execute("DROP TABLE images")
    op.execute("DROP TABLE image_likes")
    op.execute("DROP TABLE visits")
    op.execute("DROP TABLE likes")
    op.execute("DROP TABLE matches")
    op.execute("DROP TABLE conversations")
    op.execute("DROP TABLE messages")
    op.execute("DROP TABLE notifications")
