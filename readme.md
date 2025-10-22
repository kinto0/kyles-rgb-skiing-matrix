### Kyle's RGB LED Matrix in Python

Prerequisites:
 - Follow the guide [here](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/bindings/python/README.md) to
   build the python bindings for rpi-rgb-led-matrix
 - Create a `.env` file containing your [openweathermap key](https://home.openweathermap.org/users/sign_up) as `WEATHER_KEY={key}`, google maps key as GOOGLE_MAPS_API_KEY, START_LATITUDE/START_LONGITUDE for navigation start
 - run `sudo pip install -r requirements.txt`
 - add `sudo /path/to/start.sh` to your crontab to start it up on boot/schedule
