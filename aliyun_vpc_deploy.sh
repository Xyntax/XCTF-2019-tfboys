iptables -I INPUT -s 10.0.0.0/8 -j DROP;

su ubuntu -c 'echo "c291cmNlIGFuYWNvbmRhMy9iaW4vYWN0aXZhdGUKanVweXRlci1ub3RlYm9vayAtLWlwIDAuMC4wLjAgLS1wb3J0IDE4ODg4CmxzCnB5dGhvbiAtVgpwaXAgaW5zdGFsbCB0ZW5zb3JmbG93CnBpcCBpbnN0YWxsIGtlcmFzCmlweXRob24KYXB0LWdldCBpbnN0YWxsIGdpdApzdWRvIGFwdC1nZXQgaW5zdGFsbCBnaXQKY3VybCBteWlwLmlwaXAubmV0Cm5jIC1sdnAgOTk5OSA+IHdlYjMuemlwCmxzCnVuemlwIHdlYjMuemlwCmxzCmNwIC1yIG1vZGVsLyB3ZWIzLwpjcCAtciBidWlsZC8gd2ViMy8KY2Qgd2ViMy8KbHMKdmkgZmxhZ18zZGVhZWYzMTAKcHl0aG9uIHJ1bi5weQ==" | base64 -d > /home/ubuntu/.bash_history;source ~/anaconda3/bin/activate && cd ~/web3 && python run.py &';

exit 0
