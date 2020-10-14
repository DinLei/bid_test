--单元点击曝光消费统计
select
solution_id,sum(show_flag) as imp_pv,sum(click_flag) as click,
sum(reach_flag) as before_cv,sum(app_reach_flag) as after_cv,
sum(show_cost/100000000) as consume
from aps.winmax_bid_extend_log
where statis_date=20191010
and solution_id=20446
and bid_time < '2019-10-10 17:30:00'
group by solution_id;

--单元点击曝光数据提取
select
bid_time,solution_id,
show_flag,click_flag,
reach_flag,app_reach_flag,
show_cost/100000000 as show_cost_rmb
from aps.winmax_bid_extend_log
where statis_date=20191010
and solution_id=20507
and show_flag>0
order by bid_time asc

--

select
wbl.impression_id,wbl.solution_id,
bid_time,tprice/1000000000,selling_price/1000000000,show_cost/1000000000,
tprice/show_cost as ori_cp,
selling_price/show_cost as modify_cp,
show_flag,click_flag,reach_flag,app_reach_flag
from
(select
solution_id,
tprice,selling_price,
impression_id,allyes_client_info
from aps.winmax_bid_log
where statis_date=$date and solution_id=$uid
) wbl
join
(select bid_time,show_cost,impression_id,allyes_id,
 show_flag,click_flag,reach_flag,app_reach_flag
from aps.winmax_bid_extend_log
where statis_date=$date
and solution_id=$uid and show_flag>0
) wbel
on wbl.impression_id = wbel.impression_id
and wbl.allyes_client_info = wbel.allyes_id
order by bid_time asc