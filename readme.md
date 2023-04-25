# Google News
<sub>cookie-parser based on Selenium</sub>
## Start-Up
Use 
```commandline
docker build -t zmteamimage .
docker-compose up -d
```
Container ready to use. Execute in a container shell:
```commandline
python main/main.py
```

## 1.  Config
> Config module describes main env variables, 
> I should store them in .env, but ~~I'm tired~~ it would be annoying to 
> you to check
> abilities of program
## 2. db
> db module describes:
> - folder db/migrations holds migrations of the program
> - crud contains crud operations and creation of table Cookie Profile
> - db/db_processor.py contains processor of db module
> - db/run_migrations.py is a script to boot all the migrations up
> - db/utils.py is a Callback-Provided Toolkit for database
## 3. main
> main module describes:
> - main/main.py is entry-point of a program
> - main/target.py is callback-based task for worker in pool
## 4. mp_module
> mp_module describes:
> - mp_module/pool.py holds PoolFactory
> - mp_module/processor.py holds PoolExecutor, that applies tasks to pool
## 5. requests_module
> requests_module describes:
> - requests_module/NewsRequester.py holds Google News Session with proxy
> Proxy was necessary, because Google banned my computer once :) ~~Long story~~
## 6. selenium_module
> selenium_module describes:
> - selenium_module/browse.py - Browsing Processor
> - selenium_module/utils.py - utils for selenium
## 7. tests
> - testing module
# Issues
Some issues still exist. E.g. improper pool destroying and err_callback issue
