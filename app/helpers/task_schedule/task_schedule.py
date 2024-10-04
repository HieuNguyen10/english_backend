# pip install schedule  schedule==1.2.0 
import schedule
import time
import requests

def run_api_task():
    # Gọi endpoint FastAPI tại đây
    #response = requests.post('http://localhost:8080/api/v1/work_config_class/work/')
    res = requests.get("http://localhost:8080/api/v1/work_config_class/work/")
    print("API task executed.")

# Lên lịch chạy nhiệm vụ vào thời điểm cố định hàng ngày
schedule.every().day.at("20:49:00").do(run_api_task)

while True:
    print("aa")
    schedule.run_pending()
    time.sleep(1)