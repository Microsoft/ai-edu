# 这是什么项目？
这是一个可以与“黄金点”游戏服务器交互的示例客户端程序，使用 C# + [WPF](https://docs.microsoft.com/en-us/dotnet/framework/wpf/) 实现。
这个客户端提供了基本的游戏功能，比如控制游戏的进程、提交黄金点、查看历史提交数据、游戏房间管理等。

效果如下图：

![Sample image](./sample.PNG)

# 什么是“黄金点”游戏？
请在邹欣老师的博客查看游戏介绍：[创新的时机 – 黄金点游戏](https://blog.csdn.net/SoftwareTeacher/article/details/25794525)

## 我们采用的游戏规则
N个玩家，每人写一个或两个0~100之间的有理数 (不包括0或100)，提交给服务器，服务器在当前回合结束时算出所有数字的平均值，然后乘以0.618（所谓黄金分割常数），得到G值。提交的数字最靠近G（取绝对值）的玩家得到N分，离G最远的玩家得到－2分，其他玩家得0分。只有一个玩家参与时不得分。

# 我们需要哪些预备知识来阅读这些代码？
为了阅读这部分代码，我们需要：
- 对 C# 编程语言有基本的了解；
- 对 C# 的 `async/await` 编程模式有基本的了解。

同时，这些知识能更好地帮助理解这些代码：
- 对多线程操作的基本认识；
- 对 `Task`-based 异步操作的理解。
- 对 WPF 和 XAML 的了解。

# 如何让这个项目在机器上跑起来呢？
为此，我们需要：
- Windows 操作系统；
- Visual Studio 2017（推荐[可免费用于教室学习环境的 Community 版本](https://visualstudio.microsoft.com/zh-hans/vs/community/)[1]），并安装 ***.NET桌面开发*** 工作负载。

[1]: 相关的使用条款，请参见 <https://visualstudio.microsoft.com/zh-hans/license-terms/mlt553321/>。

# 配套的服务器接口介绍
下图描述了服务器如何驱动游戏一回合接着一回合的运转，同时指出了AI或客户端应何时与服务器交互。

![](./flow.png)

当AI或客户端进入游戏后，应立即向服务器请求获取当前回合的状态，此时可以知道服务器上正在进行的游戏回合的编号，以及本回合还有多长时间结束。AI或客户端可以按照返回的回合编号向服务器提交预测值，并且可以根据本回合剩余时间，设定一个定时器，在下一回合开始时，再次执行获取回合状态的接口，来取得下一回合的状态。这样依次轮转下去，AI或客户端就可以一直参与在游戏中。
同时，AI或客户端还可以在每回合开始时，调用获取历史数据的接口，来得到前几回合的比赛数据。这样可以知道自己在上一回合是否得分胜出，并可以根据历史数据来指导当前回合的预测值。

## 接口概述

服务器地址：https://goldennumber.azurewebsites.net

所有请求需要的参数都拼装在URL中，并且需要对值进行URL编码。

所有请求的响应报文内容都是JSON格式

如果服务器响应代码不是2\*\*或3\*\*，表示该次请求失败。

**失败的响应报文至少包含下面一个属性：**

属性名 | 数据类型 | 备注
-|-|-
message | String | 出错的具体信息

## 新建玩家

请求方式：GET

路径：/api/NewUser

客户端使用该接口可以新建一个玩家。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
nickName | String | 可选 | 用户昵称<br>如果长度超过20，将被截断<br>建议设置昵称，昵称相对于标识有更好的辨识度

响应报文内容中的属性：

属性名 | 数据类型 | 备注
-|-|-
userId | String | 用户标识，格式为Guid格式
nickName | String | 用户昵称

## 设置用户昵称

请求方式：POST

路径：/api/NickName

使用该接口可以用来修改用户的昵称，昵称相对于标识来说，有更佳的辩识度。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
uid | String | 必需 | 用户标识
nickname | String | 必需 | 用户昵称，长度大于20会被截断

## 获取新游戏房间

请求方式：GET

路径：/api/NewRoom

使用该接口创建一个新的游戏房间并获取对应的编号。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
uid | string | 必需 | 房间创建者的标识
numbers | Int | 可选 | 设置游戏支持的每个玩家可以提交的预测值的个数<br>默认是1，表示每个玩家可以提交一个数
duration | Int | 可选 | 设置游戏中每回合的间隔时间<br>默认值是60秒，取值范围在10~200之间
userCount | int | 可选 | 设置游戏中允许的最大玩家数<br>默认值是0，表示没有限制<br>有玩家数量限制的房间，当所有玩家都提交预测值后，会立即计算本回合结果，并开始下一轮<br>有玩家数量限制的房间，支持返回固定列数的格式化好的历史数据，未提交预测值的用0代替，但不参与计算<br>注意：这里的玩家数量限制是针对房间的，不是针对一个回合，只要玩家在房间内任一回合提交过预测值，则认为该玩家始终在房间内
roundCount | int | 可选 | 设置比赛总回合数<br>默认值是0，表示没有限制<br>如果某一回合没有玩家提交数据，认为该回合无效，不计在回合数内<br>如果有效回合数达到设置的总回合数，游戏结束，不再允许提交数据
manuallyStart | Int | 可选 | 是否手动开始游戏<br>默认值0，表示创建完房间后，游戏自动开始<br>如果是1，表示需要由创建者手动开始游戏

响应报文内容中的属性：

属性名 | 数据类型 | 备注
-|-|-
roomId | Int | 游戏房间编号

## 开始游戏

请求方式：GET

路径：/api/StartGame

如果创建游戏时设置的是手动开始，那么游戏创建者可以调用该接口开始游戏。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
uid | string | 必需 | 房间创建者的标识
roomid | int | 可选 | 房间编号<br>如果未设置，默认为0号游戏房间

## 获取游戏状态

请求方式：GET

路径：/api/State

客户端使用该接口可以获取当前房间内的游戏状态，可以根据当前游戏支持提交的预测值的个数进行提交。同时还可以知道当前回合什么时间结束，推算出什么时候可以取得本回合的比赛数据以及获取下一轮比赛的相关信息。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
uid | String | 可选 | 用户标识
roomid | Int | 可选 | 房间编号<br>如果此参数为空，默认0号房间

响应报文内容中的属性：

属性名 | 数据类型 | 备注
-|-|-
userId | String | 用户标识
nickName | String | 用户昵称
roomId | Int | 房间编号
numbers | Int | 当前房间内的游戏支持提交的预测值的个数，1或2
roundId | string | 当前房间内正在进行的游戏回合标识
leftTime | int | 当前游戏回合还有多少秒截止提交
roundEndTime | datetime | 当前回合截止提交的UTC时间
state | int | 当前游戏状态<br>0代表进行中<br>1代表未开始，需要房间创建者手动开始<br> 2代表已结束，不允许再向房间内提交数据
hasSubmitted | bool | 当前用户本回合是否已提交预测值
isRoomCreator | bool | 当前用户是否是当前房间的创建者。<br>如果房间在创建时没有指定自动开始，需要创建者手动开始游戏
maxUserCount | int | 创建房间时设定的玩家数<br>0表示没有限制<br>最大不能超过200<br>设置人数上限的房间中，在获取格式化的历史数据时，会将未加入游戏的玩家的预测值用0来填补，保证每回合取到的数据都是固定列数的规整数据<br>同时，设置人数上限的房间中，如果所有玩家都已提交，则立该结束当前回合，并开始下一回合
currentUserCount | int | 当前房间内提交过预测值的玩家数量
totalRoundCount | int | 创建房间时设定的该房间可以进行的有效回合数
finishedRoundCount | int | 当前房间内已经进行的有效回合数<br>玩家提交过预测值的回合认为是有效回合，否则忽略该回合，继续等待玩家提交

## 提交预测值

请求方式：POST

路径：/api/Submit

客户端使用该接口可以向服务器提交预测值。每回合只允许提交一次，提交成功后不可修改。

如果当前房间设置了玩家人数上限，则当所有玩家提交了预测值后，立即计算本回合结果，并开始下一回合。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
rid | String | 必需 | 要提交预测值的回合标识，需要是GUID的格式
uid | string | 必需 | 提交预测值的用户标识
n1 | Double | 必需 | 预测值，必须是0到100之间的有理数，不包括0和100
n2 | Double | 可选 | 第二个预测值，如果当前游戏是支持两个数的游戏，此参数也为必需项；如果当前游戏仅支持一个数，此参数将被忽略

## 获取历史数据

请求方式：GET

路径：/api/History

使用该接口可以获取当前房间内的历史数据，包括每回合的黄金点、每个玩家的预测值、得分等信息。

没有指定任何参数时，返回0号房间内最新的10回合的历史。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
roomid | String | 可选 | 房间编号<br>如果该参数为空，默认0号房间
startrid | String | 可选 | 开始查询的游戏回合标识<br>如果该参数为空，默认为当前正在进行的回合
count | Int | 可选 | 指定从startrid开始返回多少回合的历史，不包括startrid回合<br>如果没有指定该参数，默认为10，最大不超过100
direction | Int | 可选 | 查询的方向<br>默认值是0，表示从startrid查询旧的历史数据<br>另一个值是1，表示从startrid查询更新数据

响应报文内容中的属性：

属性名 | 数据类型 | 备注
-|-|-
rounds | Array | 查询到的回合的数组，数组的每个元素包含以下属性：<br>roundId, time, goldenNumber, userNumbers
&nbsp;&nbsp;&nbsp;&nbsp;roundId | String | 回合标识
&nbsp;&nbsp;&nbsp;&nbsp;index | int | 该回合在当前房间中的索引编号
&nbsp;&nbsp;&nbsp;&nbsp;time | String | 该回合的截止时间，UTC
&nbsp;&nbsp;&nbsp;&nbsp;goldenNumber | Double | 该回合的黄金点
&nbsp;&nbsp;&nbsp;&nbsp;userNumbers | Array | 该回合所有玩家提交的数的数组，数组的每个元素所含以下属性：<br>userId, masterNumber, slaveNumber, score
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;userId | String | 用户标识
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;masterNumber | double | 用户提交的第一个预测值
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;slaveNumber | double | 用户提交的第二个预测值，仅当当前游戏支持提交两个数的时候有效
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;score | Int | 用户在当前回合的得分
nickNames | object | 用户编号和用户昵称的字典<br>用户编号是key，用户昵称是value

## 获取格式化的历史数据

请求方式：GET

路径：/api/FormattedHistory

使用该接口可以获取当前房间内已完成的所有回合的历史数据。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
roomid | int | 可选 | 房间编号<br>如果未设置，默认为0号游戏房间

响应报文内容中的属性：

属性名 | 数据类型 | 备注
-|-|-
formattedData | string | 格式化的所有回合历史数据，该字符串是多行文本结构<br>格式举例：<br>2	5<br>18.07	30	30	17	40<br>24.87	18.08	18.08	99.9	25<br>第一行两个数表示下面有两行数据，每行数据有5个值。后面每行代表一轮比赛的数据，最后一行是最新一轮的数据。行中第一个数据是该轮的黄金点值，后面依次是是每个玩家提交的1个（或2个）预测值，数据之间以制表符分隔。如果某个值为0，表示该玩家在该轮超时未提交数据或提交数据失败
userList | array | 用户列表，数组中的每个元素包含以下属性：<br>userId, nickName, score, index
&nbsp;&nbsp;&nbsp;&nbsp;userId | string | 用户标识
&nbsp;&nbsp;&nbsp;&nbsp;nickName | string | 用户昵称
&nbsp;&nbsp;&nbsp;&nbsp;score | int | 得分
&nbsp;&nbsp;&nbsp;&nbsp;index | int | 该用户在当前房间内的索引号

## 查询得分

请求方式：GET

路径：/api/Score

使用该接口可以查询游戏房间内所有玩家的得分情况。

请求需要用到的参数：

参数名 | 数据类型 | 是否必需 | 备注
-|-|-|-
roomid | int | 可选 | 房间编号<br>如果未设置，默认为0号游戏房间

响应报文内容中的属性：

属性名 | 数据类型 | 备注
-|-|-
scoreList | array | 数组中的每个元素包含以下属性：<br>userId, nickName, score, index
&nbsp;&nbsp;&nbsp;&nbsp;userId | string | 用户标识
&nbsp;&nbsp;&nbsp;&nbsp;nickName | string | 用户昵称
&nbsp;&nbsp;&nbsp;&nbsp;score | int | 得分
&nbsp;&nbsp;&nbsp;&nbsp;index | int | 该用户在当前房间内的索引号
