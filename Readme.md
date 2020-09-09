
<p align="center">
  <a data-flickr-embed="true" href="https://www.flickr.com/photos/129776788@N07/28181453671/" title="聯紋春蜓Gomphidia confluens Selys, 1878"><img src="https://live.staticflickr.com/8674/28181453671_2e53687ae3_m.jpg" width="240" height="160" alt="聯紋春蜓Gomphidia confluens Selys, 1878"></a>
  <a data-flickr-embed="true" href="https://www.flickr.com/photos/129776788@N07/35048782976/" title="細胸珈蟌 Mnais tenuis Oguma, 1913"><img src="https://live.staticflickr.com/4195/35048782976_2b2158c72e_m.jpg" width="240" height="160" alt="細胸珈蟌 Mnais tenuis Oguma, 1913"></a>
  <a data-flickr-embed="true" href="https://www.flickr.com/photos/129776788@N07/19957114339/" title="描金晏蜓Polycanthagyna melanictera  /    Blue-faced Hawker"><img src="https://live.staticflickr.com/3743/19957114339_c0afcd6379_m.jpg" width="240" height="160" alt="描金晏蜓Polycanthagyna melanictera  /    Blue-faced Hawker"></a>
  <a data-flickr-embed="true" href="https://www.flickr.com/photos/129776788@N07/28792877864/in/album-72157668821797981/" title="夜遊蜻蜓 Tholymis tillarga (Fabircius, 1798)"><img src="https://live.staticflickr.com/8190/28792877864_f17df5b10d_m.jpg" width="240" height="160" alt="夜遊蜻蜓 Tholymis tillarga (Fabircius, 1798)"></a>

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
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
    </a>
</p>

## 1. Introduce

- Crawl the data from recording system, doing data processing and save it to the MySQL
- Print the data into google map
- Develop the GUI by ***Tkinter*** and ***PySimpleGUI***
- Plot the charts by ***matplotlib*** and ***pyecharts***

---

## 2. Include Library

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

## 3. Function

---

## 4. Demonstration

#### (1) ***Overview***

![overview](./image/program_result_picture/overview.png)

#### (2) ***Login***

![LoginPage](./image/program_result_picture/Login.PNG)

#### (3) ***Mainpage***

![Mainpage](./image/program_result_picture/mainpage.png)

#### (4) ***Plot to Google map***

![Table](./image/program_result_picture/Tablepng.png)
![GoogleMapPlot](./image/program_result_picture/googlemap.png)

#### (5) ***Save the data***

![Updating](./image/program_result_picture/Updatingpng.png)

#### (6) ***Plot by matplotlib***

- **Tree plot for species relationship**
    ![Tree plot](https://imgur.com/GIxAQAo.gif)
- **(Bar and Line plot) Species apperance among different month and year**
    ![Bar plot](https://imgur.com/6SgLY5v.png)
- **(Pie plot) Species apperance among different month and year**
    ![Pie plot](https://imgur.com/rD3qrCO.png)

#### (7) ***Plot by pyecharts***

- **Combine the map, worldcloud, bar, pie, table together**
   ![Combine pyecharts](https://imgur.com/6U8SRmN.gif)

---

## 5. License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://github.com/tingweichien" target="_blank">Ting Wei Chien</a>.
