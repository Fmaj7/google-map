import math
from celery.result import AsyncResult
from tasks import fetch_data

def generate_grid(lat_range, lng_range, step):
    lat_min, lat_max = lat_range
    lng_min, lng_max = lng_range
    lat_steps = math.ceil((lat_max - lat_min) / step)
    lng_steps = math.ceil((lng_max - lng_min) / step)
    
    grid = []
    for i in range(lat_steps):
        for j in range(lng_steps):
            lat = lat_min + i * step
            lng = lng_min + j * step
            grid.append((lat, lng))
    return grid

def main():
    keyword = "shop"
    zoom = 13
    step = 1.0
    lat_range = (-90, 90)
    lng_range = (-180, 180)
    
    grid = generate_grid(lat_range, lng_range, step)
    
    task_ids = []
    for lat, lng in grid:
        task = fetch_data.delay(lat, lng, keyword, zoom)
        task_ids.append(task.id)
    
    all_results = []
    for task_id in task_ids:
        result = AsyncResult(task_id)
        try:
            # 阻塞直到任务完成，设置超时时间，例如600秒（10分钟）
            data = result.get(timeout=600)
            all_results.extend(data)
            print(f"Fetched results for task {task_id}")
        except Exception as exc:
            print(f"Task {task_id} generated an exception: {exc}")
    
    for result in all_results:
        print(result)

if __name__ == "__main__":
    main()
