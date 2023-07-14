# Problem Description

When running `hbase hbck -details`, the following error is encountered:
```
2023-07-11 11:19:12,134 INFO  [main] client.RpcRetryingCallerImpl: Call exception, tries=6, retries=16, started=4208 ms ago, cancelled=false, msg=org.apache.hadoop.hbase.PleaseHoldException: Master is initializing
        at org.apache.hadoop.hbase.master.HMaster.checkInitialized(HMaster.java:2825)
        at org.apache.hadoop.hbase.master.MasterRpcServices.getTableDescriptors(MasterRpcServices.java:1112)
        at org.apache.hadoop.hbase.shaded.protobuf.generated.MasterProtos$MasterService$2.callBlockingMethod(MasterProtos.java)
        at org.apache.hadoop.hbase.ipc.RpcServer.call(RpcServer.java:392)
        at org.apache.hadoop.hbase.ipc.CallRunner.run(CallRunner.java:133)
        at org.apache.hadoop.hbase.ipc.RpcExecutor$Handler.run(RpcExecutor.java:354)
        at org.apache.hadoop.hbase.ipc.RpcExecutor$Handler.run(RpcExecutor.java:334)
, details=, see https://s.apache.org/timeout
2023-07-11 11:19:16,174 INFO  [main] client.RpcRetryingCallerImpl: Call exception, tries=7, retries=16, started=8248 ms ago, cancelled=false, msg=org.apache.hadoop.hbase.PleaseHoldException: Master is initializing
        at org.apache.hadoop.hbase.master.HMaster.checkInitialized(HMaster.java:2825)
        at org.apache.hadoop.hbase.master.MasterRpcServices.getTableDescriptors(MasterRpcServices.java:1112)
        at org.apache.hadoop.hbase.shaded.protobuf.generated.MasterProtos$MasterService$2.callBlockingMethod(MasterProtos.java)
        at org.apache.hadoop.hbase.ipc.RpcServer.call(RpcServer.java:392)
        at org.apache.hadoop.hbase.ipc.CallRunner.run(CallRunner.java:133)
        at org.apache.hadoop.hbase.ipc.RpcExecutor$Handler.run(RpcExecutor.java:354)
        at org.apache.hadoop.hbase.ipc.RpcExecutor$Handler.run(RpcExecutor.java:334)
, details=, see https://s.apache.org/timeout
```

When attempting to scan or perform other operations, such as `scan abc_table`, the following error is encountered:
```
ERROR: Unknown table abc_table!
```

# Usage
1. Download [hbck2.jar](https://jar-download.com/?search_box=hbck) and place it in a directory of your choice, for example `/tmp/hbase-hbck2-1.2.0.jar`.
2. Set up Python, preferably version 3.10 or above. 
3. Install the `sh` library, a useful command interative library, using `pip install sh`
4. Use any user account that has HBase operation permission. In my case, I used the hbase user.
5. Run `python fix-meta.py`, this will attempt to fix all missing regions.
6. You may need to restart HBase master for the changes made in step 5 to take effect.


# Next story
## Problem Description
- run `majar_compact 'mytable'` in hbase shell got `ERROR: No server address listed in hbase:meta for region mytable, xxxx`
- run `hbase hbck -details` got 'ERROR: Region xxxx not deployed on any region server'

## How to fix?
```bash
hbase hbck -j /tmp/hbase-hbck2-1.2.0.jar \
    assigns $(hbase hbck -details grep 'not deployed on any region server' | grep -oE  '[a-z0-9]{32}' | sort -u | tr '\n' ' ')
```

if you check the number of total regions, it should raise. now everything shoule be ok.
