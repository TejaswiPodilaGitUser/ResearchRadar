from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import settings
from app.database.base import Base

# =========================================================
# Import model modules
# =========================================================
# These imports register the tables with Base.metadata.
#
# Do NOT import paper_embedding because there is no
# PaperEmbedding model.

import app.models.paper
import app.models.author
import app.models.topic

import app.models.associations.paper_author
import app.models.associations.paper_topic


# =========================================================
# Alembic Config
# =========================================================

config = context.config


# =========================================================
# Logging
# =========================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# =========================================================
# Database URL
# =========================================================

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%"),
)


# =========================================================
# Metadata
# =========================================================

target_metadata = Base.metadata


# =========================================================
# Offline Migration
# =========================================================

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# =========================================================
# Online Migration
# =========================================================

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# =========================================================
# Run
# =========================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()