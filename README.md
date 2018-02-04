# vendor machine info getter
A python crawler running on raspberry pi to get the machine status from admin page, when status changes, the LED on the sensehat of rpi will change, and notifications will be sent out.

## File list:
| File | Usage |
| :------------ | :------------ |
|auto_orientation.py|Set the display orientation based on gravity sensors on sensehat |
|batch_getter.py| Main script |
|batch_getter_auto.sh| Shell to kick off the main script |
|config.ini| Config file for web and mail account |
|indicator.py| LED indicator for sensehat |
|README.md||
|send_mail.py|Mail sending script|
|vm_ht_getter.py| Web page crawler |
|vm_ht_getter_for_pc.py| Script running on pc to help refresh cookies |
|deploy_DB_table.sql| Create the DB and table on the first run |
|insert_into_DB.py| insert data into database|


## Usage:
1. Download this project on the raspberry pi, fill `config.ini`
2. Run `vm_ht_getter_for_pc.py` to refresh cookies
3. Transfer `cookies cookies_*.txt` to the script folder on raspberry pi
4. Run `batch_getter.py` on raspberry pi

### LED
White LED: script is trying to login
Blue LED: Login success
Green LED: machine is online
Red LED: machine is offline
Yellow LED: Login failed, need to refresh cookies

### Logs
`batch_getter_<YYYYMMDD>.log`: Script log
`last_status.log`: Log to record the last status
`batch_getter_auto.log`: Log to help track shell script


