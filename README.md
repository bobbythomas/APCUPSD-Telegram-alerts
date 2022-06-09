# APC-Telegram-alerts
APC Telegram alerts using upsfstats.cgi

  This script fetches the output from the upsfstats.cgi on the master/slave apcupsd and capture specific field value (Battery charge) and send notification to Telegram bot when there is a power outage.

  Make sure you have apcupsd package installed and configured on the Master/slave host which monitors UPS along with the apcupsd-cgi package installed. Once Apcupsd-cgi is installed properly (after apache 2 is installed) you should be able to view the upsfstats.cgi page from http://<IP address of the UPS host>/cgi-bin/apcupsd/upsfstats.cgi

  Advantage of this approach is that we don't need apcupsd client or web gui installed on the system running this code, the data is collected over the network via http.
  
  Notification alerts will be sent to telegram through Telegram bot. You will need Telegram token code and the chat id for notification via telegram bot. Please follow below for telegram bot setup.
https://gist.github.com/iwanmartinsetiawan/d10927443fcbad4ecbd2336b2e99e9de
  
  Finally thanks to https://gist.github.com/iwanmartinsetiawan and Rene from Domoticz forum (https://www.domoticz.com/forum/memberlist.php?mode=viewprofile&u=3190&sid=3dd5940c032ef638e707d2debda2da96) whose code help me develop this script.
