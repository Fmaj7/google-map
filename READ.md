1. **功能**：使用celery实现分布式异步任务，redis为broker，输入经纬度范围、关键词、缩放比例，爬取google地图商家信息: 名称、评价数、评分值、地址、电话
2. **环境**: python3, celery, redis, BeautifulSoup, selenium
3. **文件说明**:
   - `main.py`:
     - 根据步长获取区域范围经纬度，创建异步任务
   - `celery_config.py`:
     - 配置celery信息
   - `tasks.py`:
     - 具体任务：
       1. 配置Selenium WebDriver
       2. 构建谷歌地图搜索URL并打开
       3. 使用BeautifulSoup解析HTML并提取相关信息
       4. 结果返回
   - `test.py`:
     - 单独的测试文件
4. **说明**：这种数据爬取类任务，除了celery实现, 还可用多线程实现, 本例实现了商家、评价数、评分值数据抓取, 地址电话还没实现, 分析了下地址和电话存在于js中, 不在html的元素中, 可能需要别的方法实现, 有待深究
5. **celery worker运行**:
   - `celery -A tasks worker --loglevel=info`
6. **sender运行**:
   - `python main.py`
