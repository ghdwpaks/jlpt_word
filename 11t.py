
import requests
import tempfile
from bs4 import BeautifulSoup
import subprocess
import sys 

def open_kanji_detail_by_unicoded_word(unicoded_word: str):
    """
    지정한 유니코드 한자(16진수)에 대한 jitenon 검색 결과 페이지에서
    class에 'ajax'와 'color1'이 모두 포함된 첫번째 <a>의 href로 이동
    """
    url = f"https://kanji.jitenon.jp/cat/search?getdata=-{unicoded_word}-"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    print('response.status_code :',response.status_code)
    response.raise_for_status()  # 요청 실패시 예외 발생

    soup = BeautifulSoup(response.text, "html.parser")
    return_url = None
    # 모든 <a> 태그 중 class에 ajax, color1 둘 다 포함된 첫번째 태그 찾기
    for a in soup.find_all("a"):
        class_list = a.get("class", [])
        if "ajax" in class_list and "color1" in class_list:
            return_url = f"{a.get('href')}#m_kousei"
            #webbrowser.open(return_url)
            return return_url
        
    print(f"unicoded_word : {unicoded_word} / class에 'ajax'와 'color1'이 모두 포함된 <a> 태그를 찾을 수 없습니다.")
    for a in soup.find_all("a"):
        class_list = a.get("class", [])
        if "ajax" in class_list :
            return_url = f"{a.get('href')}#m_kousei"
            #webbrowser.open(return_url)
            return return_url
        
    print(f"unicoded_word : {unicoded_word} / class에 'ajax'가 모두 포함된 <a> 태그를 찾을 수 없습니다.")


def extract_kousei_parts(detail_url: str):
    """
    상세페이지에서, <span class="separator2">가 있는 <li>만,
    해당 li의 출력 텍스트(예: '广＋心')를 리스트에 담아 반환
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    res = requests.get(detail_url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    result = []
    # 모든 <li> 검사
    for li in soup.find_all("li"):
        # li 안에 <span class="separator2">가 있으면
        if li.find("span", class_="separator2"):
            text = li.get_text(strip=True)
            result.append(f"{text} = ")
    result.append(f" = ")
    return result


def open_txt_on_vscode(strings):
    # 임시 txt 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
        tmp.write('\n'.join(strings))
        tmp_filename = tmp.name

    # VSCode에서 파일 열기
    if sys.platform.startswith("win"):
        subprocess.Popen(['code', tmp_filename], shell=True)
    else:
        subprocess.Popen(['code', tmp_filename])



#원본 : 愛案以衣位囲胃印英栄塩億加果貨課芽改械害街各覚完官管関観願希季紀喜旗器機議求泣救給挙漁共協鏡競極訓軍郡径型景芸欠結建健験固功好候航康告差菜最材昨札刷殺察参産散残士氏史司試児治辞失借種周祝順初松笑唱焼象照賞臣信成省清静席積折節説浅戦選然争倉巣束側続卒孫帯隊達単置仲貯兆腸低底停的典伝徒努灯堂働特得毒熱念敗梅博飯飛費必票標不夫付府副粉兵別辺変便包法望牧末満未脈民無約勇要養浴利陸良料量輪類令冷例歴連老労録

#재정렬 후 : 不夫付必包法民無末未満約要勇良利陸料量輪類令冷例歴連老労録以位低失借伝徒働努得特的底停典加各共協争差最士氏史司臣官府管関観願信成功固完欠結建健験兵別辺変便仲置単達帯隊卒孫周祝順初兆億昨季紀希喜旗器機象照賞案愛札刷折節殺察参産散残倉貯束側続巣松梅芽菜牧種果材票標械改害街衣囲印英栄塩胃腸脈康浴養灯堂焼熱毒念敗飯飛費貨課粉副博告候航望好笑唱泣求救給挙漁軍郡径型景芸極競鏡省清静席積浅戦選然覚訓議試辞説児治


target_list = list("不夫付必包法民無末未満約要勇良利陸料量輪")#4 1
target_list = list("類令冷例歴連老労録以位低失借伝徒働努得特")#4 2
target_list = list("的底停典加各共協争差最士氏史司臣官府管関")#4 3
target_list = list("観願信成功固完欠結建健験兵別辺変便仲置単")#4 4
target_list = list("達帯隊卒孫周祝順初兆億昨季紀希喜旗器機象")#4 5
target_list = list("照賞案愛札刷折節殺察参産散残倉貯束側続巣")#4 6
target_list = list("松梅芽菜牧種果材票標械改害街衣囲印英栄塩")#4 7
target_list = list("胃腸脈康浴養灯堂焼熱毒念敗飯飛費貨課粉副")#4 8
target_list = list("博告候航望好笑唱泣求救給挙漁軍郡径型景芸")#4 9
target_list = list("極競鏡省清静席積浅戦選然覚訓議試辞説児治")#4 10



target_list = list("河液演減混潔測技採授接招提損許護講謝設評")#5 1
target_list = list("証政経績絶統編綿総素職織識鉱銭銅能態武夢")#5 2
target_list = list("賀財賛資質貧貿責貸恩快慣志性率張築報豊永")#5 3
target_list = list("逆過退適造述導桜格構査条枝検示禁祖比肥非")#5 4
target_list = list("境均基在増墓圧厚序応寄容富舎因団険限際防")#5 5
target_list = list("額預領眼規現刊券判制製則断迷情精妻婦状版")#5 6
target_list = list("可句舌居属久旧易営常暴燃災確破移程税支承")#5 7
target_list = list("仮価件個似修任備俵保仏像往衛術徳興再罪酸")#5 8
target_list = list("復複義群故敵布師飼準雑独犯効勢務益解幹耕輸余留略弁")#5 9




target_list = list("境均基在増墓圧厚序応寄容富舎因団険限際防")#5 5






for target in target_list : 

    url = open_kanji_detail_by_unicoded_word(f"{format(ord(target), '04X')}")


    parts = extract_kousei_parts(url)
    for part_idx in range(len(parts)):
        parts[part_idx] = f"{parts[part_idx]}{target}"
    open_txt_on_vscode(parts)



