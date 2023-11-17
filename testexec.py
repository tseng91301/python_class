# 定義一個空的字典，用於存儲變數
result_dict = {}

# 執行的代碼
code_to_execute = "result = 5 + 3"

try:
    # 使用 exec 執行代碼，並將局部和全局變數存儲到 result_dict 中
    exec(code_to_execute, globals(), result_dict)

    # 提取執行結果
    if 'result' in result_dict:
        output_result = result_dict['result']
        print("執行結果:", output_result)
    else:
        print("代碼未設置 'result' 變數")
except Exception as e:
    print("發生錯誤:", e)