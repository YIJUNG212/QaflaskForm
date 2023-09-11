#連資料庫的設定在這裡
HOSTNAME="127.0.0.1"
PORT=3306
USERNAME="資料庫帳號"
PASSWORD="資料庫密碼"
DATABASE="資料庫名"
DB_URI="mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI =DB_URI


#郵箱配置
MAIL_SERVER ="smtp.gmail.com"
MAIL_USE_SSL=True
MAIL_PORT =465
MAIL_USERNAME ="gmail信箱"
MAIL_PASSWORD ="在信箱上設定的app password"
MAIL_DEFAULT_SENDER ="gmail信箱"


#SECRET_KEY 範圍
SECRET_KEY="自己設定的密鑰"