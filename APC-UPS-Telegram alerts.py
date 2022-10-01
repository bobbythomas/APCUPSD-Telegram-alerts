import urllib, requests, time
from bs4 import BeautifulSoup

LINEV = "240"  # Idx for Line Voltage
BATTV = "27"  # Idx for Battery Voltage
LOADPCT = "5"  # Idx for Load Percentage
BCHARGE = "100"  # Idx for Battery Charge
#MINBATT = 10  # Set Minimum Battery value to 10%

def apc_probe():
	batt = 100  # Set the battery percentage to 100 initially
	dict = {'LINEV': LINEV, 'BATTV': BATTV, 'LOADPCT': LOADPCT,
			'BCHARGE': BCHARGE}  #
	while True:  # Endless loop
		upsfstats_status = None
		try:                                  # This keeps try connecting to the UPS host when connection error occurs or connection is interrupted.
			upsfstats_status = requests.get('http://<IP address of the UPS host>/cgi-bin/apcupsd/upsfstats.cgi')	#To connecto to the APC monitoring GUI page and collect the live output
		except requests.ConnectionError:
			print(" Received Connection Error reaching UPS host. Retrying...")
			continue
		soup = BeautifulSoup(upsfstats_status.text, 'html.parser')	#BeautifulSoup module is used to parse the HTML output
		upsfstats_parsed = soup.get_text()						#This collects the Text output from the webpage upsfstats.cgi
		formatted_output = upsfstats_parsed.split("\n", 12)[-1]	#Removes unwanted lines from the output
		result = formatted_output
		for line in result.split('\n'):
			(key, spl, val) = line.partition(': ')
			key = key.rstrip()  # Strip spaces right of text
			val = val.strip()  # Remove outside spaces
			if key in dict:  # To capture the battery value from the formatted output
				if key == 'BCHARGE':
					val = val.split(' ', 1)[0]
					batt = int(float(val))
			if key == 'STATUS' and 'ONBATT' in val:  #To check if the UPS is running on batteries.
				ups_status_message = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
				'<Telegram Token>', '<Chat ID>',
				urllib.parse.quote('UPS running on Batteries\nRemaining Battery charge: ' + str(batt)))		#Send an alert to Telegram informing that the UPS lost power.
				output = None
				try:                           # This keeps try connecting to Telegram API domain when connection error occurs or connection is interrupted.
					output = requests.get(ups_status_message, timeout=10)
				except requests.ConnectionError:
					print("Received Connection Error reaching Telegram API. Retrying...")
					continue

		time.sleep(60)  # Take a minute break. If notification interval needs to be increased, modify the sleep value accordingly (in seconds)

#Main
print("APC Probe running...")
apc_probe()
