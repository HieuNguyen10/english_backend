import httpx
from app.helpers.config import settings


def send_email(user_id, email=None, full_name=None, start_time=None, end_time=None, package_id=None):
    try:
        headers = {"Authorization": "Bearer " + settings.X_EMAIL_API_KEY}

        payload = {
            "user_id": user_id,
            "email": email,
            "full_name": full_name,
            "start_time": start_time,
            "end_time": end_time,
            "package_id": package_id
        }
        _ = httpx.post(settings.EMAIL_SERVICE, headers=headers, json=payload, timeout=10)

    except Exception as exc:
        print(exc)
        pass
