#!/bin/bash

resave_file=$1

data_sql="select bid_time,solution_id,show_flag,click_flag,reach_flag,app_reach_flag,show_cost/1000000000 as show_cost_rmb from aps.winmax_bid_extend_log where statis_date=20191008 and solution_id=20446 and show_flag>0 order by bid_time asc"

hive -e "$data_sql" | sed 's/[[:space:]]\+/,/g' > $resave_file