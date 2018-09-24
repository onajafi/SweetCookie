# Dining Bot
A better way to reserve your meal in http://dining.sharif.edu/


## This project is not fully released yet

## Setup
If you want to setup the bot on your own server follow these instructions.

This script was tested on Ubuntu 18.04
### NodeJS
If you con't have nodeJS installed, take a look at this link:

https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions

### PhantomJS & CasperJS

Checkout this link for setup instructions:

https://gist.github.com/andrewslince/4e5f9aba78e175d8fab1

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
the ```inits.py``` file, then paste the token 
instead of ```<###THE BOTS TOKEN###>``` ,
set the ```feedBack_target_chat``` variable a chat ID you like the feedbacks to be forwarded to,
 otherwise, just write 0.

Now you can run the script:

    cd SweetCookie/
    python sweetcookie.py

Run the code on the back ground so it will keep running on the server while your logged off:

    python sweetcookie.py &








