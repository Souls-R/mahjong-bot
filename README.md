# mahjong-bot 进度日志
## Day 1
>+ 打雀熟悉日本麻将规则
>
>+ 基础组件实现，设计对应类的属性和方法
>
>+ 学习如何用json序列化反序列化
>
>+ 为接入bot留好接口，~~分离server和bot~~怎么分离...
>
>+ python因为太方便而不需要支持函数重载
>
>+ 思考麻将流程
>
>+ ~~如何判断胡牌听牌？~~ 递归方法解决(比较低效就是了
>
>+ 疯狂踩pyhton list的坑 直接赋值复制list for循环中删除元素...
## Day 2
>+ python为了减少查找时的资源消耗不能省略self
>
>+ 游戏流程实现  控制台交互  输出日志
>
>+ 反应过来赢牌只能在听牌时发生，，，在其他赢法的代码上纠缠了很多冗余浪费时间。。。 思路不够清晰
>
>+ 添加了行动十分随机的AI
>
>+ 选用python-telegram-bot项目为bot框架    学习文档Tutorial（为什么没中文   搭设bot demo
>
>+ ~~为powershell设置http代理~~为tgbot的updater设置代理
>
>+ ~~tgbot在group中如何获得输入命令者的id？~~tgbot的context
## Day 3
>+ ~~尝试server与bot交互~~  没有找到通过chatid交互的方法。。。
>
>+ ~~尝试使用Pickle持久化储存~~  还是用json吧
>
>+ ~~还是缝起来做个勉强能跑的demo吧...~~  满课一天做不完了 conversationhandler还没看