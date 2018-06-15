#!/bin/sh

#1) recommended to define the variables in the environment for instance with sourcing a script, eg, . variable_exports.sh
curl -H "Client-ID $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_BEARER" -X GET 'https://api.twitch.tv/helix/streams?community_id=4912794f-4830-470f-8224-a2f793d4e5b6'


