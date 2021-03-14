# Note

1. selenium 用來執行像登入，按下一頁的動作，或是按鍵
回傳網頁資訊 = selenium.post(url, data, headers)
回傳值若要看內容-->回傳網頁資訊.text
當然也可以用 selenium.get(url. headers)來回傳資料

2. beautifulsoup用來搜尋字串，回傳即回字串，就是那行html或css
像這裡我就用id做搜尋
找到那串字串之後，如果要在解析裡面的變數值，即可以用get
像是<'XXX' = XX, 'ooo'= oo, .....>
value = soup.find(.....).get('ooo')

3. 執行 "pyinstaller -F -w --onefile .\XXXXXX.py" 將python檔案轉成 .exe檔
-w是不要出現console
--onefile是產生一個.exe檔
記得要將.exe檔從dist中拉到目錄，如果你有連結檔按圖片的話
pyinstaller -F -w  --icon=XXXX.ico .\XXXXXX.py

4. 打包轉換好的python檔案，成為一個安裝檔: NSIS
<https://www.youtube.com/watch?v=UZX5kH72Yx4>

-----------------------------------------------------------

## [2020/07/17]

紀錄一下

1. 為了使request不要都來自同一個地方，request header代表了請求的一些資訊與規範
其中的User-Agent(UA)代表了請求來源的作業系統、所使用的web driver等資訊，為了不要讓所請求的server覺得
同一個請求位置一直請求，所以使用了random的UA
<https://progressbar.tw/posts/234>
<https://ithelp.ithome.com.tw/articles/10209356>
<https://blog.csdn.net/weixin_34364135/article/details/85864318?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase>

2. 再寫傳入CSV檔時，會出現CP950的字元 error，網路上解法是用 encoding = utf-8，我這樣做雖然可以解決error
但是寫入的資料全都是亂數，所以歲後在open()中加入忽略error的指令:error ="ignore"

3. ".\\XXXXXX" 代表以現在的Folder路經基礎，也糾是相對於當前Folder的路徑

4. 如果想要print值不要換行，print("XXXX", End= "\r")

5. 正在想要怎麼加速爬蟲，可以試試用multithread

6. selenium + chromedriver 蠻好用的，指令頗直覺，像是人類在瀏覽網頁，有按鈕，填寫等功能，
其實再PTT那個範例就用過了。而session則是用url請求，也是不錯的用法

7. 搞了很久的csv發現其食用xlsx還可以很方便的指定要存哪一行或列，不用像是csv要先讀，插入，再寫入

## [2020/7/22]

1. 原本一直是要用beautifulsoup find_all 的 return list當作arg輸入map_async， 但是不知道為甚麼一直顯示can't recover from stack overflow
所以我改成直接傳一頁資訊進去，因為這樣就只需要將每個頁面的url傳進去當參數
<https://morvanzhou.github.io/tutorials/data-manipulation/scraping/4-01-distributed-scraping/>

2. 在住程式要加 \"__init\__" = \"__main\__"

3. session 是可以當參數傳遞的，也就是說如果我想要將登入動作做一次就好了，那就將登入function的session return並且在下一個韓世忠當參數傳入，
這樣那個函式就會是登入過的session
<https://stackoverflow.com/questions/26310467/python-requests-keep-session-between-function>

4. 在用 global variable時，記得要init,不然一直錯，會吃不到multiprocessing 時的 share value
<https://stackoverflow.com/questions/2080660/python-multiprocessing-and-a-shared-counter>
<http://blog.carlcarl.me/1315/python-multiprocessing-share-counter/>

5. 如果在使用 map or map_async 輸入args如果飛iterable只是想帶一個常數或不變的字串進去的話，就可以用partial

6. 用了 multiprocessing 速度至少快了一倍

7. 取小數點
<https://www.itread01.com/content/1549397542.html>

## [2020/07/26]

1. 完成looping through 整個資料庫，並依據缺少資料抓取

2. 將所抓取個廷種資料的數量記錄到json檔中，並之後依此檢查，作為Update的參考

3. Tkinter字體選擇，你可以用.config(font(字型, 大小, 粗體或斜體)
<https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-set-font-of-tkinter-text-widget/>

## [2020/07/27]

1. to quit the git in the terminal using command :q

2. Implement the multiprocessing crawling in the GUI by using \"__inti\_\_" == \"__main\_\_"
to avoid breakdown of the program

3. Finally implement the progress bar that can working independently, by using multithread
using progressbar.step(size) and progressbar.stop(), the progressbar['value'] do not work in multithread
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Progressbar.html>
<https://stackoverflow.com/questions/33768577/tkinter-gui-with-progress-bar>

4. add a Scale widget as slider bar to choose the cpu speed

5. add a group of label to display the print in Save2File

6. remember if you are going to access the label or entry or ... in one page, which is a class,
just make sure the label is in self. (self.labelName =Label(root, ....)), and then add the
method in that function for calling. Then you can access and change one widget attribute without
using global or input args.

7. Finally, finishing formatting the google map info window
<https://jupyter-gmaps.readthedocs.io/en/latest/tutorial.html>

8. remember that the callback function in combobox or Scale widget need 'event' as args, or else,
it will not react
<https://stackoverflow.com/questions/40070478/bind-combobox-to-function>

9. all the page class are inherited from tk.Frame, thus, you simply modify the Frame when define the __init__ method
<https://stackoverflow.com/questions/34817328/creating-frames-in-tkinter>

10. the entry relief style are too few  that if you want a border , you need to add a frame outside of it
<https://www.daniweb.com/programming/software-development/threads/243146/tkinter-entry-widget-border-color>

11. when the function of the widget required input args , just simply add "lambda:"
i.e. "command = lambda: your_function(input_args)"
<https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter>

12. when I move the code from old GUi to new one, the picture in canvas disappeared. Then I found that
I do not bind my canvas to the PhotoImage
<https://stackoverflow.com/questions/16846469/tkinter-canvas-image-is-not-displayed-in-class>

## [2020/08/03]

1. use checkbox to select if you want to plot the data from database to the map.

2. add the hidden password function

3. fix the error if there is no internet connection

4. few days age, I failed to convert python file to exe file, due to the marker in gmplot
can't be found. Therefore, I use batch method to auto install the libraries and execute the
python file by just click the run.bat file . Although it works, it is quite stupid

5. Finally, someone help me on the issue of pyinstaller in github by using hook to hook the gmplot, so here is the thing :

    - (1) add the folder "hooks" and put "hooks-gmplot.py" inside.-->Replace gmplot to which you want to hook
    - (2) Inside the hoo.py write:

    ```python
    from PyInstaller.utils.hooks import collect_data_files
    datas = collect_data_files('gmplot') #-->Replace gmplot to which you want to hook
    #remember not to write data = collect_data_files(C:\python\.....\gmplot) , it will raise error of invalid input
    ```

    - (3) In CMD type :
      - ```pyinstaller -F GUI_split.py --icon=.\image\dragonfly_ico.ico --additional-hooks-dir=hooks --clean``` (clean can be optional)
      - I also see the library that show my error and will hook the gmplot in the future, so that will be typing ```pip install -U pyinstaller-hooks-contrib``` solve all the problem
    - (4)reference: <https://github.com/pyinstaller/pyinstaller-hooks-contrib/issues/20>

## [2020/08/04]

1. Fix the problem for connecting to MySQL server
    (1) The connection to the MyAQL in VScode have some problem :
    ```Client does not support authentication protocol requested by server; consider upgrading MySQL client```
    (2) So to fix the error, type
    ```ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'``` Where root as your user localhost as your URL and password as your password. In my case, I put "timweiwei" as the username, "xxxxxxxx" as password and my "Dragonfly_db"as localhost.
    (3) Reference:<https://stackoverflow.com/questions/50093144/mysql-8-0-client-does-not-support-authentication-protocol-requested-by-server/50131831#50131831>

## [2020/08/10]

1. Fix the error that used my password not the password from which enter by user

2. make new .csv data file since the import to the google map with empty latitude or  longitude  will cause distortion of the position location

3. finally build up the MySQL database and insert the data into it
    ![20200810](https://i.imgur.com/Im38Y5e.png)
    reference:
    (1)<https://www.maxlist.xyz/2018/09/23/python_mysql/>
    (2)<https://realpython.com/python-sql-libraries/>

## [2020/08/14]

1. please remember to use ```#%%``` to do the cell running test

## [2020/08/17]

1. problem of showing chinese in matplotlib
    (1) check the font type in matplotlib

    ```python
    from matplotlib import font_manager
    font_set = {f.name for f in font_manager.fontManager.ttflist}
    for f in font_set:
        print(f)
    ```

    (2) check the font support for the chinese in MS website
        <https://docs.microsoft.com/en-us/typography/fonts/windows_10_font_list>
    (3)reference: <https://stackoverflow.com/questions/25561009/how-do-you-i-use-mandarin-characters-in-matplotlib>

2. select specific data in list of dictionary

    ``` python
    list(filter(lambda res: res["YEAR(Dates)"] == check_year, result))
    ```

    reference:<https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search>

## [2020/08/19]

1. successfully solved the normal distribution problem and plot the figure showing the record times in each month separated by each year.
![20200819](https://i.imgur.com/o27lGxy.png)

2. the histogram function in numpy or matplotlib  will transfer the input array into the appearance of the number, therefore, the input data should be a raw data instead of the statistics data
    ex: ```a = [1,2,1,3,4,1,5,5,6,7,8,3,1,5]```
    -->will be the desired row data to feed into hist or norm.pdf or guassin function
    ex: ```b = [4,1,2,1,3,1,1,1]```
    -->1 in```a``` show up 4 times, 2 in ```a``` show up 1 times, ......
    -->the statistic data that add up the occurrence of each number in ```a``` which will not be desired data to feed into, since the function will do the statistics again, the data plotted will be the occurrence of the occurrence of the number in ```a```
reference :
(1) <https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data>
(2) <https://stackoverflow.com/questions/11315641/python-plotting-a-histogram-with-a-function-line-on-top>
(3) <https://matplotlib.org/3.1.1/gallery/misc/table_demo.html#sphx-glr-gallery-misc-table-demo-py>

3. for the font size in the table, you need to set the auto_set_font_size to False, then you'll be able to modify the font size

    ```python
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(24)
    ```

    reference : <https://stackoverflow.com/questions/15514005/how-to-change-the-tables-fontsize-with-matplotlib-pyplot>

## [2020/08/21]

1. Using **matplotlib**
2. Add the mark and the responded text
   ![Imgur](https://i.imgur.com/6SgLY5v.png)
3. add the pie chart
   ![Imgur](https://i.imgur.com/rD3qrCO.png)
   reference :
   (1)<https://matplotlib.org/3.3.0/gallery/pie_and_polar_charts/pie_and_donut_labels.html>
   (2)<https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.patches.FancyBboxPatch.html#matplotlib.patches.FancyBboxPatch>

## [2020/08/26]

1. Using **pyecharts**
2. Add the tree plot for the species relationship
   ![Imgur](https://i.imgur.com/GIxAQAo.png)
3. there are some problem on using the radial plot that the label in half circle will not outside the node, instead, it will be inside the node.

## [2020/08/28]

### The package for integrating the html into pyhton GUI

(1) pywebview

- reference: <https://pywebview.flowrl.com/>

(2) cefpython

- reference:
  - <https://github.com/cztomczak/cefpython/blob/master/docs/Tutorial.md>
  - <https://stackoverflow.com/questions/57974532/why-cant-run-both-tkinter-mainloop-and-cefpython3-messageloop>

(3) pyhtml

- This is not work anymore

## [2020/08/30]

### The geo map visualization in python

 (1) folium

 (2) pyecharts

 (3) plotly

## [2020/08/31]

### Finally figure out how to change the simplified chinese into tradition chinese in the map by pyecharts

1. There are two version of the pyecharts, one is 0.5.11 and the        other is  v1. The 0.5.11 version is no longer maintain anymore, but   there are still  many lesson and example on the internet. The difference is that in 0.5.11 there are less feature and most of all, the v1 modify the API which group the arg or kwarg(key word arguments).

2. My problem is that I want to change the simplified chinese in the map into tradition chinese. So I start to look for maptype, and I found that in the pyecharts.datasets.map_filenames.json the "台灣" maptype is point to map\taiwan.js. However, I just couldn't find any way to get access to the file. So I turn into the older version which require plugin(pip install echart ....) from the map, and I finally can find the taiwan.js in the
   ```C:\Python37\Lib\site-packages\echarts_china_provinces_pypkg\resources\echarts-china-provinces-js```
    I modify all the simplified chinese into tradition chinese.

3. Actually, it not so complex. When I was looking for the tooltip formatter option, I found that I could modify the label by myself that I just need to change the name, the problem will be solved.

4. (**V0.5.11**)
    (1) Here is the example for the formatter and the extension installation

    ```python
    pip install echarts-countries-pypkg
    pip install echarts-china-provinces-pypkg
    pip install echarts-china-cities-pypkg
    ```

    ``` python
    import os
    from pyecharts import Map

    def tooltipformatter(params):
        return "name: " + params.name + "<br>" + "value: " + params.value

    value = [10,255]
    attr = ["台中市","嘉義縣"]
    map = Map("台灣", width=1500, height=700)
    map.add(
            "",
            attr,
            value,
            maptype='台湾',
            is_label_show=True,
            label_formatter='{b},{c}',
            is_visualmap=True,
            is_map_symbol_show=False,
            visual_text_color="#000",
            visual_range_text=["0", "255"],
            visual_range=[0, 255],
            #tooltip_formatter = '{b}, {c}'
            tooltip_formatter = tooltipformatter
            )
    map.render("map_base.html")
    os.system("map_base.html")
    ```

    reference : <https://www.lagou.com/lgeduarticle/55569.html>

    (2) The reult
    ![Taiwan tradition chinese map v0.5.11](https://i.imgur.com/DlCkzWw.png)

5. (**> V1**)
    I can't find the map_file.js,so I can only modified the label option.
   (1) I have no idea why "" is not work in JsCode, So use the '' instead.
   (2) You ```can use console.log()``` in JsCode to output the data if the code work correctly. To inspect the output goto the html file you generate and press ```F12```, it will shown in console option.
   (3) There will be no result shown if there are some bugs.
   (4) Here are my code for formatter

   ``` python
    from pyecharts.commons.utils import JsCode
    labelformatter = JsCode("""function(x){
                                var s2t = { '新北市':'新北市',
                                            '基隆市':'基隆市',
                                            '台北市':'台北市',
                                            '桃园市':'桃園市',
                                            '新竹市':'新竹市',
                                            '台中市':'台中市',
                                            '台南市':'台南市',
                                            '高雄市':'高雄市',
                                            '彰化县':'彰化縣',
                                            '嘉义市':'嘉義市',
                                            '屏东县':'屏東縣',
                                            '云林县':'雲林縣',
                                            '苗栗县':'苗栗縣',
                                            '新竹县':'新竹縣',
                                            '嘉义县':'嘉義縣',
                                            '宜兰县':'宜蘭縣',
                                            '花莲县':'花蓮縣',
                                            '台东县':'台東縣',
                                            '南投县':'南投縣',
                                            '金门县':'金門縣',
                                            '连江县':'連江縣',
                                            '中国属钓鱼岛':'釣魚島',
                                            '澎湖县':'澎湖縣'};
                                return s2t[x.name]
                            }""")

   ```

    (5) Use the formatter in the code

    ``` python
    #\ the imput data
    value=[3986291,2785159,2776846,2184655,1886465,1282669,830303,690662,554267,551816,511520,501474]
    attr = s2tFunc(["新北市", "台中市", "高雄市", "台北市", "台南市", "彰化縣", "屏東縣", "雲林縣", "苗栗縣", "新竹縣", "嘉義縣", "南投縣"])

    #\ createmap
    c = (
        Map(init_opts=opts.InitOpts(page_title="Taiwan" ,width="1600px", height="700px"))
        .add("", list(zip(attr, value)), maptype='台湾')
        .set_global_opts(title_opts=opts.TitleOpts(title="台灣"), visualmap_opts=opts.VisualMapOpts(max_=max(value)))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter='{b} : 123'))
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter=labelformatter),
            tooltip_opts=opts.TooltipOpts(formatter=tooltipformatter)
            )
        .render("map_base.html")
    )
    os.system("map_base.html")
    ```

    (6)result
    ![Taiwan tradition chinese map v1](https://i.imgur.com/2IaFqyy.png)

## [2020/09/04]

1. Successfully building up the plot with different frames, timelines

2. Charts include: Pie, bar, map, worldcloud, table.

3. Result
    ![Imgur](https://imgur.com/6U8SRmN.gif)

4. Pie
   (1) The position of Pie should be specified by ```center``` in add
   (2) The grid seems to be no use for the pie position

5. overlap
   (1) Combine the overlap for the bar and line to Timeline, can't pass the bar that overlap with the line to the Timeline. Therefore, I wrapped it with a grid then pass the grid to the timeline.

6. If the chart color do not follow then modify the ```dimension``` option

7. The structure of the chart

- tab
  - -- timeline
    - -- grid
      - -- map0
      - -- bar0
      - -- pie0
    - -- timeline2
      - worldcloud0
    - -- timeline3
      - grid_multi
        - bar_multiA
        - line_multiA
    - -- table0

8. referece :

   (1) <https://www.kesci.com/home/project/5eb7958f366f4d002d783d4a>
   (2) <https://gallery.pyecharts.org/#/Geo/geo_chart_countries_js>
   (3) <https://pyecharts.org/#/zh-cn/render_images>

## [2020/11/15]

1. Merge the branch ```Plot``` to the master

2. The ```.gitignore``` will ignore the ```Craw_data_clean``` after merging , so I am not able to merge them together

    (1) Therefore I reset the current commit, delete the content in the gitignore and recommit again

    (2) The following step shows how to do that, but one problem is that I wil not able to merge then after reset, it will do a new commit instead.

    ```
    $ git commit -m "Something terribly misguided" # (0: Your Accident)
    $ git reset HEAD~                              # (1)
    << edit files as necessary >>                  # (2)
    $ git add .                                    # (3)
    $ git commit -c ORIG_HEAD                      # (4)
    ```

    (4) When encounter the conflicts the vscode offer accept all incoming or current settings. You can access it by right clicking the file **in the chaging block** not in the **original file block**
    ![picture 2](https://i.imgur.com/2aPYnXr.png)

    (5) reference: <https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git>

## [2020/11/28]

1. Add the Plot charts option GUI

2. The command link to the ```Entry``` can be as the method of the ```StringVar``` : ```trace_Add("write", callbackFunc)``` , remember the call-back function should have three default input arguments (var, index, mode)

3. If you want to merge the branch in non fast forward: ```--no-ff```

## [2020/11/29]

### Read the doc

1. Add the readthedoc finally after a hardship.
    [readthedoc link](https://dragonfly-web-crawler.readthedocs.io/en/latest/index.html)

2. Follow the guide to install the sphinx
    [Quick start guide](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html#quick-start)

3. Init some folder and file
    - ![ReadTheDocs](https://i.imgur.com/vmKIAn6.png)
    - mkdir ```docs``` folder
    - add ```.readthedocs.yml``` in the root directory
      - i.e.

        ```python
        # Required
        version: 2

        # Build documentation in the docs/ directory with Sphinx
        sphinx:
        configuration: docs/source/conf.py

        # Build documentation with MkDocs
        #mkdocs:
        #  configuration: mkdocs.yml

        # Optionally build your docs in additional formats such as PDF
        formats:
        - pdf

        # Optionally set the version of Python and requirements required to build your docs
        python:
        version: 3.7
        install:
            - requirements: docs/requirements.txt
        ```

    - use the pip freeze to write the package into the ```requirements.txt```
        - ```pip freeze > requirements.txt```

4. The basic requirement to build for the readthedoc
    - (1) Install the **sphinx** : ```pip install sphinx```
    - (2) Add the path variable ```.....\python3\Scripts```
    - (3) Execute ```sphinx-quickstart``` in the doc folder
    - (4) Modify the file path of conf.py

        ```python
            # Build documentation in the docs/ directory with Sphinx
            sphinx:
                configuration: docs/source/conf.py
        ```

    - (5) Write the content you want to show in the file ```index.rst```
    - (6) The setting on the web will be the following
    ![setting for the readthedoc](https://i.imgur.com/1j97wmf.png)

### git rebase

1. Merge the several commits together by using ```git rebase -i IDIDIDIDIDI```

2. Push after rebase will cause problem: the HEAD is in the new branch, but the remote is in the old one
    - ![push after rebase](https://i.imgur.com/8J47j1N.png)
    - use ```git push --force```
3. reference:
   - [How to merge several commit together](https://gitbook.tw/chapters/rewrite-history/merge-multiple-commits-to-one-commit.html)
   - [push after rebase](https://stackoverflow.com/questions/8939977/git-push-rejected-after-feature-branch-rebase)

## [2020/12/1]

1. Add the link to the github, readthedocs, webpage

2. The photoImage is pretty weired

   - Remember to use the ```.png``` file
   - The instance of the photo image should be start wit ```self.```
   - You should make the instance of the PhotoImage class or else it will failed to display

       ```python
       self.ReadthedocsImg = PhotoImage(file=Index.Readthedocs_img_path)
       self.Readthedocs_Label = Label(self.Hub_parentF, text="read the docs", cursor="hand2", image=self.ReadthedocsImg, bg=Label_bg_color)
       ```

3. The alignment of the label is really tricky, I add another frame outside the label and inside the labelframe

    ```python
    #\ Hub and docs
    self.Hub_Label.pack(side=LEFT, padx=15)
    self.Readthedocs_Label.pack(side=RIGHT, padx=15)
    self.Web_version_Label.pack(side=RIGHT, padx=15)
    self.Hub_parentF.pack(expand=True)
    ```

4. result
![result add Github readthedocs and web ver](https://i.imgur.com/ilXZYQh.png)

## [2020/12/3]

1. Modify the find ID GUI: merge the latitude and longitude together

2. Add the image cover from giving urls and make it change by time
3. The website to upload image is [IMBB(https://imgbb.com/)](https://u7803223.imgbb.com/?list=images&sort=date_desc&page=1&params_hidden%5Buserid%5D=YFSvBC&params_hidden%5Bfrom%5D=user)
4. Reference:
    - [How to create a timer using tkinter?](https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter)
    - [python使用Tkinter顯示網路圖片的方法](https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/371848/)

## [2020/12/8]

1. Using multithread to fix the problem that when start to blending the images, the program will stuck and wit until it finished.
2. But still have a little bit problem on closing if it's in the thread, despite the fact that it will not have any effect currently.
3. result
![blending image](https://imgur.com/vIho7nB.gif)
4. reference:[Threading With Tkinter - Python Tkinter GUI Tutorial #97](https://www.youtube.com/watch?v=jnrCpA1xJPQ&ab_channel=Codemy.com)

## [2020/12/16]

1. Successfully use the weather api to get the history data

2. f format for using dictionary

    ```python
    f'My name {person["name"]} and my age {person["age"]}'
    ```

## [2020/12/187]

1. Delete one of the column in the MySQL database.

    ```SQL
    ALTER TABLE posts
    DROP COLUMN created_at,
    DROP COLUMN updated_at;
    ```

2. Add new column to the MySQL database

    ```SQL
    ALTER TABLE posts
    ADD COLUMN created_at;
    ```

3. Add the weather column in database. Insert the weather data in Json format. The data is get from the weather api from [World Weather Online](https://www.worldweatheronline.com/developer/my/)

4. Since this is the only one free web api fro history data.

## [2020/12/20]

1. The debugging method for the query to mysql is to user
   1. Try it on the MySQL app first by using apply.
   2. Add the error printing
    ![query debugging](https://i.imgur.com/J0ctfDX.png)

2. Add the poxy to the login request since somehow the login may be expire or timeout
    - code

        ```python
        proxy = {
           "https": 'https://220.135.64.51:8080',
            "http": 'http://220.135.64.51:8080'
        }
        r = requests.get(Index.Login_url, proxies=Index.proxy)
        ```

    - [ref](https://stackoverflow.com/questions/8287628/proxies-with-python-requests-module)
    - proxy available website : [free proxy](http://free-proxy.cz/en/proxylist/country/TW/http/ping/level3)

## [2020/12/21]

1. The image update failed in urlopen.
    - use timeout in the urlopen args to solve this

        ```python
        image_bytes = urlopen( Index.img_url_list[self.img_counter], timeout=Index.Img_timeout).read()
        ```

    - [ref](https://www.itread01.com/content/1549305566.html)

2. datetime
   - **datetime.strftime** : means string formatter, this will format a datetime object to string format.
   - **datetime.strptime** : means string parser, this will convert a string format to datetime.
   - 2 datetime difference

    ```python
    import datetime

    # datetime(year, month, day, hour, minute, second)
    a = datetime.datetime(2017, 6, 21, 18, 25, 30)
    b = datetime.datetime(2017, 5, 16, 8, 21, 10)

    # returns a timedelta object
    c = a-b
    print('Difference: ', c)

    minutes = c.total_seconds() / 60
    print('Total difference in minutes: ', minutes)

    # returns the difference of the time of the day
    minutes = c.seconds / 60
    print('Difference in minutes: ', minutes)
    ```

    result will be

    ```shell
    Difference:  36 days, 10:04:20
    Difference in minutes:  604 minutes 20 seconds
    ```

   - <https://stackoverflow.com/questions/8142364/how-to-compare-two-dates>
   - <https://www.geeksforgeeks.org/python-difference-between-two-dates-in-minutes-using-datetime-timedelta-method/>

## [2021/1/15]

1. Tk theme
   1. <https://stackoverflow.com/questions/24367710/how-do-i-change-the-overall-theme-of-a-tkinter-application>

   2. <https://wiki.tcl-lang.org/page/List+of+ttk+Themes>

   3. <https://github.com/TkinterEP/ttkthemes/blob/master/docs/themes.rst>

## [2021/1/21]

1. Add sub-progressbar to show the detailed information
   1. In Crawling date from web to the .csv file, it will show the progress of the number of each species crawling
   2. In weahter data update, it will become indeterminate mode for fun. For there are no more info need to show.
    ![update window](https://i.imgur.com/Y8sPA1U.png)

2. Add the info messagebox at the end of the crawling to info the user and to let the windows closed by pressing the button.

## [2021/1/22]

1. Add the effect that will change color when mouse hover on that frame
    ![blending_result_hover_animation](https://imgur.com/8UFWOI1.gif)

## [2021/3/6]

1. Successfully finished the code for the mutithread for weather data parsing.

2. The main problem is that when writing data to the MySQL database, although there are lock to protect different thread from commit to the
    same database, it is inside the class. This means that each instance will has it's own lock , not the lock everyone need to line up.
    So use the global lock to lwt every thread line up for the same key

3. Add a messageinfo to show if the weather crawling meet the daily limit counts.

## [2021/03/07]

1. Fix the import method by importing only the module needed

2. Add the "**key out of date**" and "**key overflow**" error message for the weather crawling

3. Change the matpltlib color map to satisfy pylint rules

    - Code

        ```python
        # piecolors = cm.coolwarm(np.linspace(0, 1, 12))
        cmap = cm.get_cmap("coolwarm")
        piecolors = cmap(np.linspace(0, 1, 12))
        ```

    - reference
      - <https://stackoverflow.com/questions/51452112/how-to-fix-cm-spectral-module-matplotlib-cm-has-no-attribute-spectral>
      - <https://stackoverflow.com/questions/47302343/what-names-can-be-used-in-plt-cm-get-cmap>
      - <https://matplotlib.org/stable/tutorials/colors/colormaps.html>

4. Solved the path problem for the tree plot in matplot.

    - File path

        ```python
        - DragonflyData
          - src
            - plot_pyecharts_tree.py
          - pyecharts_result
            - Dragonfly_tree_plot.html
        ```

    - Code

        ```python
        ../pyecharts_result/Dragonfly_tree_plot.html
        ```

## [2021/03/08]

1. Add the function to display bg of updating section
    ![Updating section](https://i.imgur.com/Ers01FW.png)

## [2021/03/14]

1. Build release program by pyinstaller
    - Remeber if the pyinstaller command is not recognized as command, then do the ```pyenv rehash``` again to let the scripts file refresh.
    <https://github.com/pyenv-win/pyenv-win/issues/67>
    ![pyenv rehash](https://i.imgur.com/7Zqi6DG.png)
    - Command
      - Not work command

        ``` python
        pyinstaller -F src\GUI_split.py --icon=.\docs\image\dragonfly_ico.ico --add-data="C:\Users\Admin\.pyenv\pyenv-win\versions\3.7.3\Lib\site-packages\pyecharts\render\templates\.;.\templates" --add-data="C:\Users\Admin\.pyenv\pyenv-win\versions\3.7.3\Lib\site-packages\pyecharts\datasets\.;.\datasets" --additional-hooks-dir=hooks --clean
        ```

      - Command
        - Release mode:

            ``` python
            pyinstaller -F src\GUI_split.py --distpath="./" -n="Dragonfly-Data" --icon=.\docs\image\dragonfly_ico.ico --additional-hooks-dir=hooks -w --clean
            ```

        - Debug mode:

            ```python
            pyinstaller -F src\GUI_split.py --distpath="./" -n="Dragonfly-Data-debug" --icon=.\docs\image\dragonfly_ico.ico --additional-hooks-dir=hooks --clean
            ```

      - problem
        - Reguired including the pyecharts
            **Final Solution** : <https://www.cnblogs.com/LoveOpenSourceBoy/p/14192260.html>
            (Other solution not work : <https://blog.csdn.net/u013586693/article/details/109455581>)
            ![problem 2](https://i.imgur.com/J1kyfX0.png)

        - The output .exe file path
            **Solution** : <https://pyinstaller.readthedocs.io/en/stable/usage.html>
            ![problem 4](https://i.imgur.com/EUXpKTG.png)
