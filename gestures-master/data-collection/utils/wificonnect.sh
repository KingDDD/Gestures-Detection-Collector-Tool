#!/bin/bash
#
#   Connects the PEQ to the wifi
#   Created on April 26, 2017
#-------------------------------------------------------------------------------
#   Copyright (c) 201x Magic Leap, Inc. (COMPANY) All Rights Reserved.
#   Magic Leap, Inc. Confidential and Proprietary
#
#   NOTICE:  All information contained herein is, and remains the property
#   of COMPANY. The intellectual and technical concepts contained herein
#   are proprietary to COMPANY and may be covered by U.S. and Foreign
#   Patents, patents in process, and are protected by trade secret or
#   copyright law.  Dissemination of this information or reproduction of
#   this material is strictly forbidden unless prior written permission is
#   obtained from COMPANY.  Access to the source code contained herein is
#   hereby forbidden to anyone except current COMPANY employees, managers
#   or contractors who have executed Confidentiality and Non-disclosure
#   agreements explicitly covering such access.
#
#   The copyright notice above does not evidence any actual or intended
#   publication or disclosure  of  this source code, which includes
#   information that is confidential and/or proprietary, and is a trade
#   secret, of  COMPANY.   ANY REPRODUCTION, MODIFICATION, DISTRIBUTION,
#   PUBLIC  PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE  OF THIS
#   SOURCE CODE  WITHOUT THE EXPRESS WRITTEN CONSENT OF COMPANY IS
#   STRICTLY PROHIBITED, AND IN VIOLATION OF APPLICABLE LAWS AND
#   INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF  THIS SOURCE
#   CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS
#   TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
#   USE, OR SELL ANYTHING THAT IT  MAY DESCRIBE, IN WHOLE OR IN PART.
#-------------------------------------------------------------------------------
#   This will connect the PEQ to wifi-demo, so that the computer
#   can access the peq via wifi.
#
#   USAGE:
#   ./wifi_connect.sh
#
#   Created on April 26, 2017
#   author="Seung Jung Jin"

mldb devices
mldb shell "stop universe"

OUTPUT="$(mldb shell wificmd -z)"
echo $OUTPUT
if [[ $OUTPUT == *"Failure"* ]]; then
    echo "Adding firewall rules"
    mldb shell "ip rule add from all fwmark 0x0/0xffff lookup main"
    echo "... enabling wifi ..."
    mldb shell "wificmd -o t=1,s=2"
    echo "... verifying wifi enabled ... "
fi

read -p "Is this the first time connecting to the wifi after flashing(y/n)? " answer
case ${answer:0:1} in
    y|Y )
        mldb shell "wificmd -z"
        echo "... Scanning wifi networks ..."
        mldb shell "wificmd -o, S,s=4"
        echo "... adding wifi-demo ..."
        mldb shell "wificmd -a -n wifi-demo -p alderaan -o hi"
        echo "... listing networks ..."
        mldb shell "wificmd -l"
        echo "... assuming id 0 is wifi-demo and connecting ..."
        mldb shell "wificmd -i 0 -o c,s=1"
    ;;
    * )
	echo "... Skipping initial setup ..."
    ;;
esac

echo "... changing port to 5555 ..."
mldb tcpip 5555
sleep 5
echo "... getting ip adress ..."
ip="$(mldb shell ifconfig | grep -A 1 'wlan0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
echo "... connecting to peq $ip ..."
mldb connect $ip:5555
echo "... Make sure to disconnect the USB cable ..."

