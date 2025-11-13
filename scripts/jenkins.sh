# cd auto-web-test
rm -rf allure-results
sleep 1m
weekday=$(date +%u)
hour=$(date +%H)
if [ "$weekday" -eq 4 ] && [ "$hour" -ge 19 ] && [ "$hour" -le 23 ] && [ "$smoke"="only_Thursday" ]||[ "$smoke"="yes" ];then
	echo "仅准运行冒烟测试"
	python utils/change_round.py ${feishu_receive_id} $base_url normal
  pytest -vgs --alluredir=allure-results --tracing=on -video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on --maxschedchunk=1
else
	echo "运行全量测试"
	python utils/change_round.py ${feishu_receive_id} $base_url normal
	set +e
	pytest -vgs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url -persistent=on --maxschedchunk=1 --maxschedchunk=1
    pytest -vgs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url-$base_url -persistent=on
	set -e
	python utils/change_round.py ${feishu_receive_id} $base_url 变更v3
	set +e
    pytest -vas --alluredir=allure-results --tracing=on -video=retain-on-failure --screenshot=only-on-failure --base-url=sbase url --persistent=on
	set -e
	python utils/change_round.py ${feishu_receive_id} $base_url 拟制v3
	set +e
	pytest -vgs --alluredir=allure-results --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on --maxschedchunk=1  --tracing=on
    pytest -vgs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on --maxschedchunk=1
    set -e
    python utils/change_round.py ${feishu_receive_id} $base_url normal
fi