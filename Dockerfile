FROM    ubuntu:12.04
# Make sure the package repository is up to date
RUN     echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN     apt-get update

# Install vnc, xvfb in order to create a 'fake' display and firefox
RUN     apt-get install -y x11vnc xvfb firefox
RUN     mkdir ~/.vnc
# Setup a password
RUN     x11vnc -storepasswd 1234 ~/.vnc/passwd
# Autostart firefox (might not be the best way to do it, but it does the trick)
RUN     bash -c 'echo "firefox" >> /.bashrc'
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/TheFedExpress/data602-assignment2 /usr/src/app/trading
EXPOSE 5000
CMD [ "python", "/usr/src/app/trading/TradingApp2.py" ]