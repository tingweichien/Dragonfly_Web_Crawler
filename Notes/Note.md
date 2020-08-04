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

5. 正在想要怎麼加速爬蟲，可以試試用mutithread

6. selenium + chromedriver 蠻好用的，指令頗直覺，像是人類在瀏覽網頁，有按鈕，填寫等功能，
其實再PTT那個範例就用過了。而session則是用url請求，也是不錯的用法

7. 搞了很久的csv發現其食用xlsx還可以很方便的指定要存哪一行或列，不用像是csv要先讀，插入，再寫入

## [2020/7/22]

1. 原本一直是要用beautifulsoup find_all 的 return list當作arg輸入map_async， 但是不知道為甚麼一直顯示can't recover from stackover flow
所以我改成值節傳一頁資訊進去，因為這樣就只需要將每個頁面的url傳進去當參數
<https://morvanzhou.github.io/tutorials/data-manipulation/scraping/4-01-distributed-scraping/>

2. 在住程式要加__init__ = __main__

3. session 是可以當參數傳遞的，也就是說如果我想要將登入動作做一次就好了，那就將登入function的session return並且在下一個韓世忠當參數傳入，
這樣那個函式就會是登入過的seesion
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

1. to guit the git in the terminal using command :q

2. impliment the multiprocessing crawling in the GUI by using "__inti__" == "__main__"
to avois breakdown of the program

3. Finally impliement the progress bar that can working independently, by using multithread
using progressbar.step(size) and progressbar.stop(), the progressbar['value'] do not work in multithred
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Progressbar.html>
<https://stackoverflow.com/questions/33768577/tkinter-gui-with-progress-bar>

4. add a Scale widget as slider bar to choose the cpu speed

5. add a group of label to display the print in Save2File

6. remember if you are going to access the label or entry or ... in one page, which is a class,
just make sure the label is in self. (self.labelName =Label(root, ....)), and then add the
method in that function for calling. Then you can access and change one widget attirbute without
using global or input args.

7. Finally, finishing formating the google map info window
<https://jupyter-gmaps.readthedocs.io/en/latest/tutorial.html>


8. remember that the callback function in combobox or Scale widget need 'event' as args, or else,
it will not react
<https://stackoverflow.com/questions/40070478/bind-combobox-to-function>

9. all the page class are inherited from tk.Frame, thus, you simply mosify the Frame when defing the __init__ method
<https://stackoverflow.com/questions/34817328/creating-frames-in-tkinter>

10. the entry relief style are too few  that if you want a border , you need to add a frame outside of it
<https://www.daniweb.com/programming/software-development/threads/243146/tkinter-entry-widget-border-color>

11. when the function of the widget required input args , just simply add "lambda:"
i.e. "command = lambda: your_function(input_args)"
<https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter>

12. when I move the code from old GUi to new one, the picture in canvas dissapeared. Then I found that
I do not bind my canvas to the PhotoImage
<https://stackoverflow.com/questions/16846469/tkinter-canvas-image-is-not-displayed-in-class>

## [2020/08/03]

1. use checkbox to select if you want to plot the data from databae to the map.

2. add the hidden password function

3. fix the error if there is no internet connection

4. few days age, I failed to convert python file to exe file, due to the marker in gmplot
can't be found. Therefore, I use batch method to auto install the libraries and execute the
python file by just click the run.bat file . Although it works, it is quite stupid

5. Finally, someone help me on the issue of pyinstaller in github by using hook to hook the gmplot, so here is the thing :

    (1)add the folder "hooks" and put "hooks-gmplot.py" inside.-->Replace gmplot to which you want to hook
    (2) Inside the hoo.py write:

    ```python
    from PyInstaller.utils.hooks import collect_data_files
    datas = collect_data_files('gmplot') #-->Replace gmplot to which you want to hook
    #remember not to write datas = collect_data_files(C:\python\.....\gmplot) , it will raise error of invalid input
    ```

    (3) In CMD type :
    ```pyinstaller -F GUI_split.py --icon=.\image\dragonfly_ico.ico --addtional-hooks-dir=hooks --clean (clean can be optional)```
I also see the library that show my error and will hook the gmplot in the future, so that will be typing ```pip install -U pyinstaller-hooks-contrib``` solve all the problem

    (4)reference: <https://github.com/pyinstaller/pyinstaller-hooks-contrib/issues/20>



## [2020/08/04]

1. The connection to the MyAQL in VScode have some problem :
    ```Client does not support authentication protocol requested by server; consider upgrading MySQL client```
    so to fix the error, type
    ```ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'``` Where root as your user localhost as your URL and password as your password
    In my case, I put "timweiwei" as the username, "xxxxxxxx" as password and my "Dragonfly_db"
    as localhost
    reference:<https://stackoverflow.com/questions/50093144/mysql-8-0-client-does-not-support-authentication-protocol-requested-by-server/50131831#50131831>