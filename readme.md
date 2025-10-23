### Kyle's RGB LED Matrix in Python

Prerequisites:
 - `uv venv && source .venv/bin/activate`
 - Follow the guide [here](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/bindings/python/README.md) to
   build the python bindings for rpi-rgb-led-matrix
 - Create a `.env` file containing your [openweathermap key](https://home.openweathermap.org/users/sign_up) as `WEATHER_KEY={key}`, google maps key as GOOGLE_MAPS_API_KEY, START_LATITUDE/START_LONGITUDE for navigation start
 - run `uv pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple` (make sure to add pywheels as an index)
 - add `sudo /path/to/start.sh` to your crontab to start it up on boot/schedule
