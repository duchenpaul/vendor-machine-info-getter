#!/bin/bash
cd /home/pi/run/vm_ht_getter/vm_ht_indicator/
/home/pi/run/vm_ht_getter/vm_ht_indicator/batch_getter.py >> /home/pi/run/vm_ht_getter/vm_ht_indicator/batch_getter_auto.log 2>&1
