import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import time

# Streamlitのヘッダーと説明
st.title('Yahoo Japan 自動ログイン（SMS認証付き）')
st.write('Yahoo Japanのログイン情報を入力してください。')

# ユーザーからの入力を取得
email = st.text_input('Yahooメールアドレス')

if st.button('ログイン'):
    # WebDriverのセットアップ
    options = ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモードを使用
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome_service = fs.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=options)

    try:
        # Yahoo Japanのログインページにアクセス
        driver.get('https://login.yahoo.co.jp/')

        # メールアドレスの入力 (最新の識別子を確認する必要があります)
        email_input = driver.find_element(By.XPATH, '//input[@name="username"]')
        email_input.send_keys(email)
        driver.find_element(By.ID, 'btnNext').click()
        time.sleep(5)

        # SMS認証の処理
        st.write('SMS認証コードを入力してください。')
        sms_code = st.text_input('SMS認証コード')

        if sms_code:
            # SMS認証コードの入力フィールドを確認する必要があります
            sms_input = driver.find_element(By.XPATH, '//input[@name="verificationCode"]')
            sms_input.send_keys(sms_code)
            driver.find_element(By.ID, 'btnSubmit').click()
            time.sleep(5)

            st.write('ログイン成功！')

    except Exception as e:
        st.error(f"ログインに失敗しました: {e}")
    finally:
        driver.quit()

