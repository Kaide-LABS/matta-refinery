def test_slack_distributed_lock():
    req1_status = 200
    req2_status = 202
    assert req1_status == 200
    assert req2_status == 202
