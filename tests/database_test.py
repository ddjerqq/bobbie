import asyncio

from rgbprint import rgbprint

from models.database import Database
from models.user import User


class DbTest:
    @staticmethod
    async def get_user_test():
        database = Database()
        await database.ainit()
        user = User.create(725773984808960050, "ddjerqq")

        get = await database.user_service.get(user.id)

        try:
            assert get == user
        except AssertionError:
            rgbprint("[-] User gotten from databse is not same", color="red")
        else:
            rgbprint("[+] get_user_test passed successfully", color="green")




async def main():
    await DbTest.get_user_test()

if __name__ == "__main__":
    asyncio.run(main())
