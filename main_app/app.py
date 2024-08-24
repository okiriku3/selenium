# coding:utf-8
#https://ohenziblog.com/streamlit_cloud_for_selenium/

# 必要なパッケージのインポート
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By

# タイトルを設定
st.title("seleniumテストアプリ")

# ボタンを作成(このボタンをアプリ上で押すと"if press_button:"より下の部分が実行される)
press_button = st.button("スクレイピング開始")

if press_button:
    # スクレイピングするwebサイトのURL
    #URL = "https://ohenziblog.com"
    URL = "https://furusato-iiyama.net/a278/"

    # ドライバのオプション
    options = ChromeOptions()

    # option設定を追加（設定する理由はメモリの削減）
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # webdriver_managerによりドライバーをインストール# chromiumを使用したいのでchrome_type引数でchromiumを指定しておく
    
    CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    service = fs.Service(CHROMEDRIVER)
    driver = webdriver.Chrome(
                              options=options,
                              service=service
                             )

    # URLで指定したwebページを開く
    driver.get(URL)
    #URLで指定したwebのタイトルを取得

    title = driver.title

    # webページ上のタイトル画像を取得
    img = driver.find_element(By.TAG_NAME, 'img')
    src = img.get_attribute('src')

    # 取得した画像をカレントディレクトリに保存
    with open(f"tmp_img.png", "wb") as f:
        f.write(img.screenshot_as_png)

    # 保存した画像をstreamlitアプリ上に表示
    st.image("tmp_img.png")

    # webページを閉じる
    driver.close()

    # スクレピン完了したことをstreamlitアプリ上に表示する
    st.write('Website title:', title)
    st.write("スクレイピング完了!!!")

#below is by chatgpt
import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service as fs
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import time

# Streamlitアプリの設定
st.title('Ebookjapan Screenshot to PDF Converter')

# 入力フォーム
email = st.text_input("Enter your Yahoo email:", "")
sms_code = st.text_input("Enter the SMS code (you will receive it during login):", "")
book_url = st.text_input("Enter the URL of the ebook:", "")
submit_button = st.button("Start Capturing")

if submit_button and email and sms_code and book_url:
    # Streamlit UIで実行中のメッセージ
    st.write("Logging in and capturing pages... Please wait.")

    # WebDriver Managerを使用してChromeDriverを自動インストール
    try:
        # ChromeDriverのパスを取得
        chrome_service = fs.Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        # Chromeオプションを設定
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')

        # ブラウザを起動
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # Yahoo! Japanのログインページにアクセス
        driver.get("https://login.yahoo.co.jp/config/login")

        # メールアドレスの入力
        email_input = driver.find_element(By.ID, "login-username")
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        time.sleep(5)  # SMSコード入力画面に移動するまで待機

        # SMS認証コードの入力
        sms_input = driver.find_element(By.ID, "verification-code")  # SMSコードの入力フィールドのIDを指定
        sms_input.send_keys(sms_code)
        sms_input.send_keys(Keys.RETURN)

        time.sleep(5)  # 認証が完了するまで待機

        # 書籍のURLを開く
        driver.get(book_url)

        # ページが完全にロードされるのを待機
        time.sleep(5)

        # 保存する画像リスト
        images = []

        # ページ送りとキャプチャのループ
        while True:
            # スクリーンショットを取得
            screenshot = driver.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot))
            images.append(image)

            try:
                # 次のページボタンを探してクリック
                next_button = driver.find_element(By.CLASS_NAME, 'next-button-class-name')  # 次のページボタンのクラス名を指定
                next_button.click()
            except:
                # 次のページボタンが見つからない場合は最終ページと判断してループ終了
                break

            # ページが変わるまで待機
            time.sleep(3)

        # PDFとして保存
        pdf_path = 'ebookjapan_screenshots.pdf'
        images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=100.0)

        # PDFダウンロードリンクの表示
        st.success("PDF Capturing complete!")
        with open(pdf_path, "rb") as file:
            st.download_button(label="Download PDF", data=file, file_name="ebookjapan_screenshots.pdf", mime="application/pdf")
        
        # ブラウザを終了
        driver.quit()

    except Exception as e:
        st.error(f"Failed to start ChromeDriver: {e}")
