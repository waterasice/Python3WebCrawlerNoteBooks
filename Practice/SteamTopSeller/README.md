# 要求

1 .爬虫：爬取 https://store.steampowered.com/search/?category1=998&filter=topsellers 热销游戏数据制作数据集

2 .需要爬取数据

- (1)游戏名
- (2)游戏公司
- (3)好评等级
- (4)评论人数（购买人数）
- (5)语言种类
- (6)价格
- (7)发行时间
- (8)系统需求
- (9)游戏标签

# 遇到的问题

- re 匹配失败，匹配词不精准
- request 的 get 方法失败，原因是成人验证，需要加入 cookies 。
- 爬取速度慢