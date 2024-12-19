import uuid
from sqlmodel import SQLModel, Field


class AuthUser(SQLModel, table=True):
    """_summary_
        CREATE TABLE IF NOT EXISTS public.auth_user
        (
            id uuid NOT NULL,
            phone_number character varying COLLATE pg_catalog."default" NOT NULL,
            jwt_token character varying COLLATE pg_catalog."default" NOT NULL,
            expiration_time integer NOT NULL,
            CONSTRAINT auth_user_pkey PRIMARY KEY (id)
        )

        CREATE UNIQUE INDEX IF NOT EXISTS ix_auth_user_phone_number
        ON public.auth_user USING btree
        (phone_number COLLATE pg_catalog."default" ASC NULLS LAST)
        TABLESPACE pg_default;
    """
    __tablename__ = "auth_user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    phone_number: str = Field(unique=True, nullable=False, index=True)
    jwt_token: str = Field(nullable=False)
    expiration_time: int = Field(nullable=False) 
