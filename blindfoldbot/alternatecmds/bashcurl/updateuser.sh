#!/bin/sh

#1) recommended to define the variables in the environment for instance with sourcing a script, eg, . variable_exports.sh
curl -H "Client-ID $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_BEARER" -X PUT "https://api.twitch.tv/helix/users?description=$1"


