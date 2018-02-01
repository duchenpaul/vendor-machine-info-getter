# vendor machine info getter
A python crawler running on raspberry pi to get the machine status from admin page, when status changes, the LED on the sensehat of rpi will change, and notifications will be sent out.

## File list:
| File | Customized value? | Usage |
| :------------ | :------------ | :------------ |
|auto_orientation.py||Set the display orientation based on gravity sensors on sensehat |
|batch_getter.py |Y| Main script |
|batch_getter_auto.sh|Y| Shell to kick off the main script |
|config.ini|Y| Config file for web account |
|indicator.py|| LED indicator for sensehat |
|README.md|||
|send_mail.py|Y|Mail sending script|
|vm_ht_getter.py|| Web page crawler |
|vm_ht_getter_for_pc.py|| Script running on pc to help refresh cookies |


## Usage:
1. Download this project on the raspberry pi
2. Run `vm_ht_getter_for_pc.py` to refesh cookies
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



##TODO
Modify the script `vm_ht_getter_for_pc.py` to read parameters from config file
