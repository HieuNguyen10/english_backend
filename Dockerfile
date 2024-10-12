FROM python:3.10-slim

# Đặt thư mục làm việc cho app
WORKDIR /app

# Copy file requirements.txt
COPY requirements.txt .

# Cài đặt các dependencies
RUN pip install -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Tạo nhóm và người dùng mới
RUN groupadd -g 1000 app_group
RUN useradd -g app_group --uid 1000 app_user

# Thay đổi quyền sở hữu thư mục
RUN chown -R app_user:app_group /app

# Chuyển sang người dùng không phải root
USER app_user

# Chạy Alembic revision và upgrade trước khi chạy app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
