from .database import engine, Base, async_session
from .schemas import Group, Permission

# Create/Drop all models/migrations in DBM.
async def init():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        """async with async_session() as session:
            async with session.begin():
                session.add_all(
                    [
                        Group(
                            name='Administradores',
                            code_name='admins',
                        ),
                        Group(
                            name='Usuarios',
                            code_name='users'
                        )
                    ]
                )"""