#!/bin/sh
#Need an "app token" to do this, not the regular access token, so the command as written below doesn't work.
#1) recommended to define the variables in the environment for instance with sourcing a script, eg, . variable_exports.sh
#curl -H "Client-ID $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_BEARER" -X POST 'https://api.twitch.tv/helix/entitlements/upload?manifest_id=7658&type=bulk_drops_grant'


