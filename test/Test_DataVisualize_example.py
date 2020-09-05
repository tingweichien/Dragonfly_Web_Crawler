
import matplotlib as mp
import pandas as pd


#%%
import numpy as np
import matplotlib.pyplot as plt
# prepare the data
x = np.linspace(0, 10, 100)
y = x

# plot the data
plt.plot(x, y, label='linear')
plt.legend()
plt.title("title")
plt.suptitle("subtitle")
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# %%
x2 = np.arange(2,12,1)
y2=2*x2
plt.subplot(211)
plt.plot(x2, y2, 'ro',label="-linear")
plt.subplot(212)
plt.plot(x, y, label='linear')
plt.xlim(0,12)
plt.ylim(0, 20)

# %%
plt.style.use('bmh')
x3 = np.linspace(0, 10, 100)
y3 = np.sin(x3)
y4 = np.cos(x3)
plt.plot(x3, y3, x3, y4)
plt.legend(['sin','cos'])

# %%
hist = np.random.randn(1000)
plt.hist(hist, edgecolor='LightSteelBlue', bins=30)

# %%
data = [10, 20, 50, 5, 15]
label = ['A', 'B', 'C', 'D', 'E']
explode = [0, 0, 0, 0.05, 0]
plt.pie(data, labels=label, explode=explode, autopct="%.1f%%")

# %%
lists = [('1', 2434), ('10', 6792), ('11', 5214), ('12', 3354), ('2', 2854), ('3', 5571), ('4', 5602), ('5', 5768), ('6', 7320), ('7', 7341), ('8', 7198), ('9', 6878)]
print(zip(*lists))
x, y = zip(*lists) # unpack a list of pairs into two tuples
x_months=['Jan', 'Oct', 'Nov', 'Dec', 'Feb', 'March', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept']

plt.bar(x_months, y, color='b')
plt.xticks(x_months, x_months, rotation='vertical')
plt.tight_layout()
plt.show()

# %%
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ["225 g flour",
          "90 g sugar",
          "1 egg",
          "60 g butter",
          "100 ml milk",
          "1/2 package of yeast"]

data = [225, 90, 50, 60, 100, 5]

wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title("Matplotlib bakery: A donut")

#
# %%
import os
import json

from pyecharts import options as opts
from pyecharts.charts import Page, Tree

data = [
        {
            "children": [
                {"name": "B"},
                {
                    "children": [
                        {"children": [{"name": "I"}], "name": "E"},
                        {"name": "F"},
                    ],
                    "name": "C",
                },
                {
                    "children": [
                        {"children": [{"name": "J"}, {"name": "K"}], "name": "G"},
                        {"name": "H"},
                    ],
                    "name": "D",
                },
            ],
            "name": "A",
        }
    ]

tree=(
     Tree()
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"))
    )

tree.render()

# %%
l = [1,2,3,4]
print(['name']*len(l))
print(tuple(zip(['name']*len(l),l)))
A = zip(['name']*len(l),l)
B = dict(A)
print(B)


# %%
import webview


def open_file_dialog(window):
    file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')

    result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
    print(result)


if __name__ == '__main__':
    window = webview.create_window('Open file dialog example', 'https://pywebview.flowrl.com/hello')
    webview.start(open_file_dialog, window)


#%%
import webview


html = """
    <style>
        body {
            background-color: #333;
            color: white;
            font-family: Helvetica Neue, Helvetica, Arial, sans-serif;
        }

        .main-container {
            width: 100%;
            height: 90vh;
            display: flex;
            display: -webkit-flex;
            align-items: center;
            -webkit-align-items: center;
            justify-content: center;
            -webkit-justify-content: center;
            overflow: hidden;
        }

        .loading-container {
        }

        .loader {
          font-size: 10px;
          margin: 50px auto;
          text-indent: -9999em;
          width: 3rem;
          height: 3rem;
          border-radius: 50%;
          background: #ffffff;
          background: -moz-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: -webkit-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: -o-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: -ms-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: linear-gradient(to right, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          position: relative;
          -webkit-animation: load3 1.4s infinite linear;
          animation: load3 1.4s infinite linear;
          -webkit-transform: translateZ(0);
          -ms-transform: translateZ(0);
          transform: translateZ(0);
        }
        .loader:before {
          width: 50%;
          height: 50%;
          background: #ffffff;
          border-radius: 100% 0 0 0;
          position: absolute;
          top: 0;
          left: 0;
          content: '';
        }
        .loader:after {
          background: #333;
          width: 75%;
          height: 75%;
          border-radius: 50%;
          content: '';
          margin: auto;
          position: absolute;
          top: 0;
          left: 0;
          bottom: 0;
          right: 0;
        }
        @-webkit-keyframes load3 {
          0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
          }
          100% {
            -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
          }
        }
        @keyframes load3 {
          0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
          }
          100% {
            -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
          }
        }

        .loaded-container {
            display: none;
        }


    </style>
    <body>
      <div class="main-container">
          <div id="loader" class="loading-container">
              <div class="loader">Loading...</div>
          </div>

          <div id="main" class="loaded-container">
              <h1>Content is loaded!</h1>
          </div>
      </div>

      <script>
          setTimeout(function() {
              document.getElementById('loader').style.display = 'none'
              document.getElementById('main').style.display = 'block'
          }, 5000)
      </script>
    </body>
"""


if __name__ == '__main__':
    window = webview.create_window('Loading Animation', html=html, background_color='#333333')
    webview.start()

# %%
import threading
import time
import sys
import random
import webview


html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<style>
    #response-container {
        display: none;
        padding: 3rem;
        margin: 3rem 5rem;
        font-size: 120%;
        border: 5px dashed #ccc;
    }

    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }

    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
        text-transform: uppercase;
    }

</style>
</head>
<body>


<h1>JS API Example</h1>
<p id='pywebview-status'><i>pywebview</i> is not ready</p>

<button onClick="initialize()">Hello Python</button><br/>
<button id="heavy-stuff-btn" onClick="doHeavyStuff()">Perform a heavy operation</button><br/>
<button onClick="getRandomNumber()">Get a random number</button><br/>
<label for="name_input">Say hello to:</label><input id="name_input" placeholder="put a name here">
<button onClick="greet()">Greet</button><br/>
<button onClick="catchException()">Catch Exception</button><br/>


<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>pywebview</i> is ready'
    })

    function showResponse(response) {
        var container = document.getElementById('response-container')

        container.innerText = response.message
        container.style.display = 'block'
    }

    function initialize() {
        pywebview.api.init().then(showResponse)
    }

    function doHeavyStuff() {
        var btn = document.getElementById('heavy-stuff-btn')

        pywebview.api.doHeavyStuff().then(function(response) {
            showResponse(response)
            btn.onclick = doHeavyStuff
            btn.innerText = 'Perform a heavy operation'
        })

        showResponse({message: 'Working...'})
        btn.innerText = 'Cancel the heavy operation'
        btn.onclick = cancelHeavyStuff
    }

    function cancelHeavyStuff() {
        pywebview.api.cancelHeavyStuff()
    }

    function getRandomNumber() {
        pywebview.api.getRandomNumber().then(showResponse)
    }

    function greet() {
        var name_input = document.getElementById('name_input').value;
        pywebview.api.sayHelloTo(name_input).then(showResponse)
    }

    function catchException() {
        pywebview.api.error().catch(showResponse)
    }

</script>
</body>
</html>
"""


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def getRandomNumber(self):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(random.randint(0, 100000000))
        }
        return response

    def doHeavyStuff(self):
        time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': 'Operation cancelled'}
                break
        else:
            then = time.time()
            response = {
                'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
            }
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True

    def sayHelloTo(self, name):
        response = {
            'message': 'Hello {0}!'.format(name)
        }
        return response

    def error(self):
        raise Exception('This is a Python exception')



if __name__ == '__main__':
    api = Api()
    window = webview.create_window('API example', html=html, js_api=api)
    webview.start()




