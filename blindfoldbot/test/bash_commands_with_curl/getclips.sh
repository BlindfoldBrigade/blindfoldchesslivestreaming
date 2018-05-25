#!/bin/sh

#1) recommended to define the variables in the environment for instance with sourcing a script, eg, . variable_exports.sh
curl -H "Client-ID $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_BEARER" -X GET "https://api.twitch.tv/helix/clips?broadcaster_id=$TWITCH_BROADCASTER_NAME"


