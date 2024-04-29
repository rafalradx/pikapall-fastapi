import unittest
from fastapi import HTTPException, status
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas.users import UserIn
from src.repository.users import UserRepository


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.users_repository = UserRepository(db_session=self.session)
        # self.user = User(id=1)

    async def test_get_user_by_email_found(self):
        user = User(email="drajkata@op.pl")
        self.session.query().filter().first.return_value = user
        result = await self.users_repository.get_user_by_email(email="drajkata@op.pl")
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await self.users_repository.get_user_by_email(email="drajkata@op.pl")
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserIn(username="drajkata", email="drajkata@op.pl", password="drajkata1")
        result = await self.users_repository.create_user(new_user=body)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        user = User(email="drajkata@op.pl")
        token = "12345678900987654321"
        await self.users_repository.update_token(user=user, token=token)
        self.session.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
