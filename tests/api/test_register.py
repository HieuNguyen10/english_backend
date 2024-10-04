import random

from starlette.testclient import TestClient
from tests.faker.fake_provider import fake

from app.helpers.config import settings
from app.helpers.enums import UserRole


class TestRegister:
    def test_success(self, client: TestClient):
        """
            Test controller users register success
            Step by step:
            - Gọi API Register với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
        """
        register_data = {
            'full_name': fake.name(),
            'email': fake.email(),
            'password': 'secret123',
            'role': random.choice(list(UserRole)).value
        }
        print(f'[x] register_data: {register_data}')
        r = client.post(f"{settings.API_PREFIX}/register", json=register_data)
        print(f'[x] Response: {r.json()}')
        assert r.status_code == 200
        response = r.json()
        assert response['code'] == '000'
        assert response['message'] == 'Thành công'
        assert response['data']['email'] is not None
