
import requests
import tempfile
from bs4 import BeautifulSoup
import subprocess
import sys 

import ast


from tkinter.filedialog import askopenfilename

import re


from datetime import datetime




def extract_kanji(text: str) -> str:
    return "".join(re.findall(r'[\u4E00-\u9FFF]', text))



def read_until_ctrl_c():
    buffer = []
    print("입력을 시작하세요. Ctrl + C 를 누르면 종료됩니다.\n")

    try:
        while True:
            line = input()
            buffer.append(line)
    except KeyboardInterrupt:
        pass  # 입력 종료

    result = "\n".join(buffer)

    result = extract_kanji(result)

    return result



text = read_until_ctrl_c()
selected_kanji = list(set(text))




base_info_file = askopenfilename(title="정보 원천 파일 선택", filetypes=[("All Files", "*.*")])

if not base_info_file:
    raise RuntimeError("파일지정이 안됐습니다.")


base_info_txt_data = ""
with open(base_info_file, "r", encoding="utf-8") as f:
    base_info_txt_data = f.read().strip()
base_info_list:list = ast.literal_eval(base_info_txt_data)




target_data = []

for value in selected_kanji:
    matched = next((row for row in base_info_list if row["k"] == value), None)
    if matched:
        target_data.append(matched)
    else:
        #없으면
        target_data.append({'k':value,'s':'','m':'','km':'','mm':'','mu':''})


print(target_data)
              






result = []


for d in target_data : 
    if not d['km'] == '' :
        #훈독이 없는 한자인 경우
        result.append(f"\"{d['k']}\",\"{d['km']}\",\"{d['s']}\",\"\"") #態,(형)태,たい,
    elif not d['m'] == '': 
        #훈독이 있는 한자인 경우
        m_base_list = d['m'].split("·")
        m_res_list = []
        for m in m_base_list :
            only_kanji_sound = [x for x in list(m) if x not in list(d['mu'][m])]
            only_kanji_sound = "".join(only_kanji_sound)
            m_temp_res = f"({only_kanji_sound}){d['mu'][m]}"#(た)絶える
            m_temp_res = f"{m_temp_res}:{d['mm'][m]}"#(た)絶える:끊어지다
            m_res_list.append(m_temp_res)

        m_res = ' / '.join(m_res_list)

        result.append(f"\"{d['k']}\",\"{m_res}\",\"{d['s']}\",\"\"")
    else :
        #애초부터 못찾은 경우
        result.append(f"\"{d['k']}\",\"\",\"\",\"\"")


#T,D,P,E
now = datetime.now()
m = int(f"{now.minute:02d}")//10
timenow = f"{now.month:02d}{now.day:02d}_{now.hour:02d}_{m}"
with open(f"mext/ops/daily/{timenow}.csv", "w", encoding="utf-8") as f:
    
    f.write("T,D,P,E" + "\n")
    for item in result:
        f.write(item + "\n")




            




