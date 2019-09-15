#%%
# chromedriverはbrewなどでインストールしておく
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import pathlib
import yaml
import sys

#%%
# ------------------
# コマンドの入力チェック
# ------------------
args = sys.argv

if(len(args) <= 1):
    print("設定ファイルのパスが指定されていません")
    sys.exit()
elif len(args) == 2:
    filepath = args[1]
    if filepath.endswith(".yaml"):
        with open(filepath) as file:
            yml = yaml.safe_load(file)
    else:
        print("設定ファイルの形式が不適切です。YAML形式のファイルを指定して下さい。")
        sys.exit()
else:
    print("オプションの指定が不適切です。")

#%%
# -------------------------
# 設定ファイルから変数を読み込む
# -------------------------

# 対象となる月
target_month = str(yml['target']['month']) # 例："4"(４月の場合）

# 請求書(領収書)発行日
bill_year = str(yml['bill_date']['year']) # 例:"2019"
bill_month = "{:02d}".format(yml['bill_date']['month'])  # 例: "04"
bill_day = "{:02d}".format(yml['bill_date']['day'])  # 例: "19"

# Benefit station関連情報
benefit_id = str(yml['benefit']['id'])
benefit_pass = str(yml['benefit']['pass'])

# すくすく関連情報
Sukusuku_number = str(yml['sukusuku']['number'])
child_name = str(yml['sukusuku']['child_name'])
birth_year = str(yml['sukusuku']['birth_year'])
birth_month = "{:02d}".format(yml['sukusuku']['birth_month']) 
birth_day = "{:02d}".format(yml['sukusuku']['birth_day']) 

# 請求書/領収書関連情報
kijun = str(yml['bill_info']['kijun']) # "1":領収書発行月を基準として申請する
bill_monthly_amount = str(yml['bill_info']['bill_monthly_amount'])
apply_monthly_amount = str(yml['bill_info']['apply_monthly_amount'])
nursley_school = str(yml['bill_info']['nursley_school'])

# 銀行口座情報
bank_name = str(yml['bank']['name'])
bank_branch = str(yml['bank']['branch'])
bank_type = str(yml['bank']['type']) # 普通
bank_account_number = str(yml['bank']['account_number'])
bank_account_name = str(yml['bank']['account_name'])

# 申込者情報
postcode = str(yml['applicant']['postcode'])
prefecture = str(yml['applicant']['prefecture']) # 東京都
address1 = str(yml['applicant']['address1']) 
address2 = str(yml['applicant']['address2']) 
email1 = str(yml['applicant']['email1']) 
email2 = str(yml['applicant']['email2']) 
telephone_type = str(yml['applicant']['telephone_type'])  # 携帯
telephone_num = str(yml['applicant']['telephone_num'])

# 証明書
syoumei_method = str(yml['syoumei']['method'])
directory_path = str(yml['syoumei']['directory'])

print("設定ファイルからパラメータの読み込みが完了しました")

#%%
# ------------------------------
# 対象のページにbrowserでログインする
# ------------------------------

# Start Chrome browser
driver = webdriver.Chrome()

# Open Benefit Station top page
url_top = "https://bs.benefit-one.co.jp/bs/pages/bs/top/top.faces"
driver.get(url_top)
time.sleep(3)

# User Login
driver.find_element_by_id("cmnHederForm:textfield").send_keys(benefit_id)
driver.find_element_by_id("cmnHederForm:textfield2").send_keys(benefit_pass)
driver.find_element_by_id("cmnHederForm:textfield2").send_keys(Keys.ENTER)

# Access to target web page "Suku Suku monthly"
url = "https://bs.benefit-one.co.jp/bs/pages/bs/srch/menuPrticSrchRslt.faces?menuNo=642245"
driver.get(url)
time.sleep(3)

driver.find_element_by_class_name("container_btnset").click()
time.sleep(3)

# ブラズザの別ウィンドウに遷移する
handle_array = driver.window_handles
driver.switch_to.window(handle_array[1])
driver.current_url

# Select "agree" element
driver.find_elements_by_tag_name("a")[1].click()
time.sleep(3)


print("ログインが完了しました")

#%%
# -----------------------
# フォームに入力する（その１）
# -----------------------

# すくすく倶楽部へ登録はお済ですか
driver.find_element_by_name("myForm:_idJsp101:0:_idJsp135").click()

# お子様名
driver.find_element_by_id("myForm:_idJsp101:1:_idJsp119").send_keys(child_name)

# お子様の誕生日
birth_year_element = driver.find_element_by_name("myForm:_idJsp101:2:_idJsp120")
Select(birth_year_element).select_by_value(birth_year)

birth_month_element = driver.find_element_by_name("myForm:_idJsp101:2:_idJsp124")
Select(birth_month_element).select_by_value(birth_month)

birth_day_element = driver.find_element_by_name("myForm:_idJsp101:2:_idJsp128")
Select(birth_day_element).select_by_value(birth_day)

# 申請期限の申請基準
kijun_element = driver.find_element_by_name("myForm:_idJsp101:3:_idJsp132")
Select(kijun_element).select_by_value(kijun)

# 請求書の対象月
target_month_element = driver.find_element_by_name("myForm:_idJsp101:4:_idJsp132")
Select(target_month_element).select_by_value(target_month)

# 請求書の発行年月日
bill_year_element = driver.find_element_by_name("myForm:_idJsp101:5:_idJsp120")
Select(bill_year_element).select_by_value(bill_year)

bill_month_element = driver.find_element_by_name("myForm:_idJsp101:5:_idJsp124")
Select(bill_month_element).select_by_value(bill_month)

bill_day_element = driver.find_element_by_name("myForm:_idJsp101:5:_idJsp128")
Select(bill_day_element).select_by_value(bill_day)

# 領収書額面
driver.find_element_by_id("myForm:_idJsp101:6:_idJsp119").send_keys(bill_monthly_amount)

# 申請額面
driver.find_element_by_id("myForm:_idJsp101:7:_idJsp119").send_keys(apply_monthly_amount)

# 利用施設名
driver.find_element_by_id("myForm:_idJsp101:8:_idJsp119").send_keys(nursley_school)

# 銀行名
driver.find_element_by_id("myForm:_idJsp101:11:_idJsp119").send_keys(bank_name)

# 支店名
driver.find_element_by_id("myForm:_idJsp101:13:_idJsp119").send_keys(bank_branch)

# 口座種別
bank_type_element = driver.find_element_by_name("myForm:_idJsp101:14:_idJsp132")
Select(bank_type_element).select_by_value(bank_type)

# 口座番号
driver.find_element_by_id("myForm:_idJsp101:15:_idJsp119").send_keys(bank_account_number)

# 口座名義
driver.find_element_by_id("myForm:_idJsp101:16:_idJsp119").send_keys(bank_account_name)


# 誓約にチェックつける
# 「おむつ代、おやつ代、延長料金、送迎料金等月極保育料以外の料金は含まれていません
driver.find_element_by_name("myForm:_idJsp101:18:_idJsp135").click()

# 月極め保育料以外の申請内容が含まれている場合は補助金額が減額されることがあります。
driver.find_element_by_name("myForm:_idJsp101:19:_idJsp135").click()

# 証明書提出方法
syoumei_element = driver.find_element_by_name("myForm:_idJsp101:20:_idJsp132") 
Select(syoumei_element).select_by_value(syoumei_method)

# ファイルアップロード

# ターゲットのディレクトリからファイル一覧を取得
p = pathlib.Path(directory_path)
file_list =[]
for file in p.iterdir():
    if (file.name).startswith('.'):
        pass
    else:
        absolute_filename = str(file.resolve())
        file_list.append(absolute_filename)

# 取得したファイル一覧をフォームに入力
if len(file_list) == 1:
    driver.find_element_by_name("myForm:_idJsp101:21:_idJsp140").send_keys(file_list[0])
elif len(file_list) == 2:
    driver.find_element_by_name("myForm:_idJsp101:21:_idJsp140").send_keys(file_list[0])
    driver.find_element_by_name("myForm:_idJsp101:22:_idJsp140").send_keys(file_list[1])
elif len(file_list) == 3:
    driver.find_element_by_name("myForm:_idJsp101:21:_idJsp140").send_keys(file_list[0])
    driver.find_element_by_name("myForm:_idJsp101:22:_idJsp140").send_keys(file_list[1])
    driver.find_element_by_name("myForm:_idJsp101:23:_idJsp140").send_keys(file_list[2])
else:
    print("対象のフォルダに3個より多く含まれています。不要なファイルがないか確認してください")
    sys.exit()

print("フォーム１の入力が完了しました")

#%%
# 次へボタンを押す
driver.find_element_by_id("myForm:_idJsp147").click()

#%%
# -----------------------
# フォームに入力する（その２）
# -----------------------

# 郵便番号
driver.find_element_by_id("memberInfoRegistModifyInputForm:zipCode").send_keys(postcode)

# 住所（都道府県）
prefecture_element = driver.find_element_by_id("memberInfoRegistModifyInputForm:prefe")
Select(prefecture_element).select_by_value(prefecture)

# 住所（市区町村番地）
driver.find_element_by_id("memberInfoRegistModifyInputForm:cdtvAddr").send_keys(address1)

# 住所(マンション名)
driver.find_element_by_id("memberInfoRegistModifyInputForm:builName").send_keys(address2)

# E-mail
driver.find_element_by_id("memberInfoRegistModifyInputForm:acnt").send_keys(email1)
driver.find_element_by_id("memberInfoRegistModifyInputForm:dmin").send_keys(email2)

# E-mail confirm
driver.find_element_by_id("memberInfoRegistModifyInputForm:_idJsp363").send_keys(email1)
driver.find_element_by_id("memberInfoRegistModifyInputForm:_idJsp364").send_keys(email2)

# Telephone
telephone_type_element = driver.find_element_by_name("memberInfoRegistModifyInputForm:_idJsp365")
Select(telephone_type_element).select_by_value(telephone_type)

driver.find_element_by_id("memberInfoRegistModifyInputForm:telProtyOne").send_keys(telephone_num)

#%%

print("フォーム２の入力が完了しました")
