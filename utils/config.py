import torndb

from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="dorkoo", help="database name")
define("mysql_user", default="haha", help="database user")
define("mysql_password", default="123qwes", help="database password")

db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

browser = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'