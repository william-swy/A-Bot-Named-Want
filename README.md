# **Discord Bot**

## **Description**
A discord bot for your server

Made with Discord.py

### **Functions**
* Plays music based on song name(Uses Youtube API to query for URL and song title)
* Adds new music to a queue
* Pause, resume and skip music at your leisure
* Get the current weather of a city
* Schedules weather reports
* Welcomes new members

### **Usage**
1. Download ffmpeg and add to PATH
2. create `.\Discord-Bot\data\.env` file with discord, youtube API and openweathermap tokens 
(use `.\Discord-Bot\data\template.env`) as template if desired
3. Run Bot Command and Weather Report configs, see instructions below
4. run `main.py` and type `?help` to see full list of commands

### **Configure Bot Command Prefix**
1. Run `src\config_prefix.py`
2. Input your one letter prefix

### **Configure Timed Weather Reports**
1. Run `src\config_weather.py`
2. Input city names, `<city name>`. Add `<state code, ISO 3166 country code>` to input if need to specify
3. Input UTC times as in 24 hour format(ie. `02:00` for 2:00 am and `14:00` for 2:00 pm)
