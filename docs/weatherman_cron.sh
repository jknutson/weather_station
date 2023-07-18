#!/bin/bash
set -eou pipefail

source .env.local # SAS_TOKEN should be in here
export PGUSER=jknutson
export PGHOST=localhost
export PGDATABASE=mn-gis-projects

WORKING_DIR=/opt/weatherman

pushd $WORKING_DIR

case $1 in
        5min|10min)
        echo "select wm_update_latest_readings();" | psql > /dev/null
        echo "select json_agg(wm_latest_readings)->0 from wm_latest_readings where station='pico' limit 1" | psql -t -o ./current_conditions.json
        curl -s -X PUT -d "@./current_conditions.json" -H "x-ms-date: $(TZ=GMT date '+%a, %d %h %Y %H:%M:%S %Z')" -H "x-ms-blob-type: BlockBlob" "https://weatherman.blob.core.windows.net/%24web/current_conditions.json${SAS_TOKEN}"
        ;;

        hourly)
        echo "select wm_update_hourly_summaries();" | psql > /dev/null
        echo "\copy (select * from wm_readings_24_hours) to ${WORKING_DIR}/last_24_hours.csv csv header;" | psql > /dev/null
        cp "${WORKING_DIR}/last_24_hours.csv" /var/www/html/weatherdata/
        curl -s -X PUT -d "@./last_24_hours.csv" -H "x-ms-date: $(TZ=GMT date '+%a, %d %h %Y %H:%M:%S %Z')" -H "x-ms-blob-type: BlockBlob" "https://weatherman.blob.core.windows.net/%24web/last_24_hours.csv${SAS_TOKEN}"
        ;;

esac

popd

# MAILTO="john.m.knutson@gmail.com"
# 10 * * * * OUT=`echo "select wm_update_hourly_summaries();" | psql -h localhost -U jknutson -d mn-gis-projects` || echo "$OUT"
# */5 * * * * OUT=`/opt/weatherman/weatherman_cron.sh 5min` || echo "$OUT"
# # */5 * * * * OUT=`echo "select wm_update_latest_readings();" | psql -h localhost -U jknutson -d mn-gis-projects` || echo "$OUT"
# # */5 * * * * OUT=`echo "\copy (select json_agg(wm_latest_readings)->0 from wm_latest_readings where station='pico' limit 1) to stdout" | psql -h localhost -U jknutson -d mn-gis-projects > /var/www/html/latest_readings.json` || echo "$OUT"
# 30 3 * * * OUT=`echo "VACUUM VERBOSE ANALYZE;" | psql -h localhost -U jknutson -d mn-gis-projects` || echo "$OUT"
# 15 * * * * OUT=`echo "\copy (select * from wm_readings_24_hours) to '/var/www/html/weatherdata/last_24_hours.csv' csv header;" | psql -U jknutson -d mn-gis-projects -h localhost` || echo "$OUT"
# 5 2 * * * OUT=`echo "select wm_update_yesterday_daily_summaries();" | psql -h localhost -U jknutson -d mn-gis-projects` || echo "$OUT"
