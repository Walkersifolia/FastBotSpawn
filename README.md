# FastBotSpawn
-----

一个[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)插件，可以批量召唤假人并设置前缀，最好与fabric-carpet的配置项fakePlayerNamePrefix保持一致。

依赖于fabric-carpet

### 指令
```
!!b set bot_ 设置前缀，bot_可替换，推荐和Carpet配置同步，没有就留空
!!b clear 清除设置的前缀
!!b spawn [mini] [max] 批量召唤假人
!!b drop [mini] [max] 批量控制丢出全部物品
!!b kill [mini] [max] 批量下线假人
[mini] [max] 是最小和最大的序号，差值不能超过10，不写默认为1-10
```
