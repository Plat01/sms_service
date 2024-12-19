from sqlalchemy import select, ext
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import AuthUser


class UserCrud:

    @staticmethod
    async def create_new_record(
        session: AsyncSession, phone_number: str, jwt_token: str, expiration_time: int
    ) -> AuthUser:
        
        new_record = AuthUser(
            phone_number=phone_number,
            jwt_token=jwt_token,
            expiration_time=expiration_time,
        )
        try:
            session.add(new_record)
            await session.commit()
        except ext.IntegrityError as e:
            print(e)
        await session.refresh(new_record)
        return new_record
    
    @staticmethod
    async def create_or_update_record(
        session: AsyncSession, phone_number: str, jwt_token: str, expiration_time: int
    ) -> AuthUser:
        """Create or update a record by phone number.

        Args:
            session (AsyncSession): session fo DI
            phone_number (str): _description_
            jwt_token (str): JWT in string format
            expiration_time (int): int in seconds from start of epoch

        Returns:
            AuthUser: user object
        """
        record = await UserCrud.get_by_phone_number(session, phone_number)
        if record:
            record.jwt_token = jwt_token
            record.expiration_time = expiration_time
            await session.commit()
        else:
            record = await UserCrud.create_new_record(
                session, phone_number, jwt_token, expiration_time
            )
        return record


    @staticmethod
    async def get_by_phone_number(session: AsyncSession, phone_number: str) -> AuthUser | None:
        """Retrieve a record by phone number."""
        query = select(AuthUser).where(AuthUser.phone_number == phone_number)
        result = await session.execute(query)
        return result.scalar_one_or_none()