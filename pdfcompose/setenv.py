import os

# 设置环境变量
os.environ["TEST_ENV"] = "FDSFJHDSJKFHJDSFHJS"

# 读取一个特定的环境变量
env_variable_value = os.getenv("TEST_ENV")

# 如果环境变量不存在，你可以提供一个默认值
env_variable_value = os.getenv("PATH", "DEFAULT_VALUE")

# 打印环境变量的值
print("环境变量的值:", env_variable_value)