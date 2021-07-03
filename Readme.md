
<p align="center">
  <a data-flickr-embed="true" href="https://www.flickr.com/photos/129776788@N07/28181453671/" title="聯紋春蜓Gomphidia confluens Selys, 1878"><img src="https://live.staticflickr.com/8674/28181453671_2e53687ae3_m.jpg" width="240" height="160" alt="聯紋春蜓Gomphidia confluens Selys, 1878"></a>


</p>

</p>
<h1 align="center">Dragonfly Web Crawler</h1>
<p align="center">
    <em>Python 3.7.3</em>
</p>

<p align="center">
    <a href="https://ci.appveyor.com/project/tingweichien/dragonfly-web-crawler">
        <img src="https://ci.appveyor.com/api/projects/status/81cbsfjpfryv1cl8/branch/master?svg=true" alt="Appveyor Build Status">
    </a>
     <a href="https://github.com/pyecharts/pyecharts/pulls">
        <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="Contributions welcome">
    </a>
    <a href='https://dragonfly-web-crawler.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/dragonfly-web-crawler/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
    </a>
</p>



## 1. Introduce

- Crawl the data from recording system, doing data processing and save it to the MySQL database.
- Print the data on google map.
- Develop the GUI by ***Tkinter*** and ***PySimpleGUI***.
- Plot the charts by ***matplotlib*** and ***pyecharts***.

---

## 2. Installation

- Execute the ```Dragonfly-Data.exe``` to run the program.
![start](./docs/image/program_result_picture/start.png)

- Open ```Dragonfly-Data-debug.py``` or ```.\src\GUI_split.py``` debug it.

---

## 3. Include Library

- Web Crawler:
  - **requests**
  - **bs4 (BeautifulSoup)**
  - **selenium (webdriver)**

- Data Processing
  - **re**
  - **numpy**

- GUI
  - **Tkinter**
  - **PySimpleGui**
  - **webbrowser**

- Data Saving
  - **csv**
  - **json**
  - **multiprocessing**
  - **mysqul.connector**

- Charts Plotting
  - **matplotlib**
  - **pyecharts**

- Executable file
  - **pyinstaller**

---

## 4. File function

|File|Function|
|--|--|
|GUI_split.exe |The executive file for the program|
|GUI_split.py|The main GUI file|
|GUI_split.spec|File specify for pyinstaller|
|Dragonfly.py|For web crawler|
|DataClass.py|The class declaration for the data|
|Database.py|Write or read from the MySQL database|
|Save2File.py|Save(Write) or read the data to or from CSV file|
|Index.py|The file to store variable for setting|
|hook.py <br> .hooks\     |The links for the libraries to hooks to do ptinstaller|
|.Crawl_Data\ <br> .Crawl_Data_clea\ | The data crawl from the web store in csv|
|update_chromdriver.py|Tto update the chromedriver to satisfy with the current chrome version|
---

## 5. Demonstration

#### (1) ***Overview***

![overview](./docs/image/program_result_picture/overview.png)

#### (2) ***Login***

![LoginPage](./docs/image/program_result_picture/Login.PNG)

#### (3) ***Waiting***

![WaitingPage](https://i.imgur.com/li0ydJu.png)

#### (4) ***Mainpage***

![Mainpage](https://i.imgur.com/inTKauJ.png)

#### (5) ***Plot to Google map***

![Table](./docs/image/program_result_picture/Tablepng.png)
![GoogleMapPlot](./docs/image/program_result_picture/googlemap.png)

#### (6) ***Save the data***

![Updating](https://i.imgur.com/rTNEyS2.png)

#### (7) ***Plot by matplotlib***

- **Tree plot for species relationship**
    ![Tree plot](https://imgur.com/GIxAQAo.gif)
- **(Bar and Line plot) Species apperance among different month and year**
    ![Bar plot](https://imgur.com/6SgLY5v.png)
- **(Pie plot) Species apperance among different month and year**
    ![Pie plot](https://imgur.com/rD3qrCO.png)

#### (8) ***Plot by pyecharts***
- **Overview**
  ![pyecharts overview](https://i.imgur.com/toAw1z1.png)

- **Combine the map, worldcloud, bar, pie, table together**
  ![Combine pyecharts](https://imgur.com/6U8SRmN.gif)

---

## 5. License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://github.com/tingweichien" target="_blank">Ting Wei Chien</a>.
