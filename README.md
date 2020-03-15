# option-price-web-demo
This is a web demo to show the futures option price under django frame.

## Code of Local Running
1. 切换到 Python3 环境，可以用虚拟环境 virtualenv，总之要确认 `python --version` 的输出是 `Python3` 字样

	```console
	$ python --version
	Python 3.7.6
	$ pip --version
	pip 20.0.2 from /Users/FDUHYJ/anaconda3/envs/option/lib/python3.7/site-packages/pip (python 3.7)
	```

1. 切换回本项目的根目录，安装 pip 依赖

	```console
	$ ls
	LICENSE          README.md        baoqian          requirements.txt

	$ pip install -r requirements.txt
	```

1. 切换到 baoqian 目录，初始化数据库

	```console
    $ cd baoqian
	$ ls
	README.md apps      baoqian   data      db_tools  locale    manage.py static    templates
	$ python manage.py migrate
	$ python manage.py flush --noinput
	$ python db_tools/initdb.py
	```

1. 运行站点，浏览器访问：`http://127.0.0.1:8000/`

	```console
	$ python manage.py runserver
	...
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
	```