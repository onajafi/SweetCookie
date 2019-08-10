# Sweet Cookie
A better way to reserve your meal in [dining.sharif.edu](http://dining.sharif.edu/)

## About
In our university (Sharif University of Technology) 
most students are able to purchase their lunch or dinner 
with a cheap price from the _Universities Dining Institution_. However, 
the meal must be purchased 4 days before the time it is served.

So every time we had to open the browser and reach to [dining.sharif.edu](http://dining.sharif.edu/), 
login to our own dining account (Entering username and password), 
navigate to the reservation section and click on every meal we wanted for a specific day.

This comes with a problem, A lot of us used to forget the reservation 
due time and ended up dealing with higher priced meals or in some cases starvation :O

There were different solutions to this problem, the most simplest one 
was that every time someone noticed the reservation time, he or she would 
send a message to others as a reminder of the reservation time. Some used 
to set an alarm. Most of these solutions were useful and were good enough 
but it still required the user to login and do all the reservation process 
which was explained above. Most of the time we were getting distracted 
from reserving the meals and forgetting to complete the reservation process.

Until one day everything changed...

Introducing **SweetCookie**

![Sweet Cookies Logo](https://raw.githubusercontent.com/onajafi/SweetCookie/Release/_images/SweetCookiesLogo.png)

SweetCookie is the name of a _web crawling_ bot which means it has the ability
to navigate in different websites as a human user and perform the same tasks that 
an ordinary user does on a website (e.g. Clicking, Logging in), it uses this 
ability to navigate into [dining.sharif.edu](http://dining.sharif.edu/). The bot 
also has a Telegram Bot Interface so the users can control the bot 
in a user-friendly environment.

The bot is written in Python combined with the 
[CapserJS](http://casperjs.org/)
 framework (Javascript).
The CasperJS framework is a powerful tool which handles the web crawling tasks.

Try the bot at this address: [t.me/Sweet_Cookie_Bot](t.me/Sweet_Cookie_Bot)


## Setup
If you want to setup the bot on your own server follow these instructions.

This script was tested on Ubuntu 18.04
### NodeJS
If you don't have nodeJS installed, take a look at this link:

https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions

### PhantomJS & CasperJS

Checkout this link for setup instructions:

https://gist.github.com/onajafi/60499a2a7749fe4af4fa19d2b377bc08

### Telegram API python library

[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) is used to connect with the servers of Telegram, issue this commend to install it on your system:

```pip2 install pyTelegramBotAPI```

if you don't have pip installed, checkout [this link](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/#installing-pip-for-python-2).

### python emoji library

```pip2 install emoji```

### Clone the repo and initialize the script
Issue this command to get the script:

```git clone https://github.com/onajafi/SweetCookie.git```

In Telegram create your bot using [BotFather](https://core.telegram.org/bots#6-botfather).

After getting your bots TOKEN, copy it and open 
the ```python/inits.py``` file, then paste the token 
instead of ```<###THE BOTS TOKEN###>``` ,
set the ```feedBack_target_chat``` variable a chat ID you like the feedbacks to be forwarded to,
 otherwise, just write 0.

Now you can run the script:

    cd SweetCookie/python
    python sweetcookie.py

Run the code on the back ground so it will keep running on the server while you're logged off:

    python sweetcookie.py &








