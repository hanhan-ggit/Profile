# Quantumult X 自定义保护方案检查表

本文档作为独立于主配置的开发维护文档，记录了从上游 `ddgksf2013/Profile` 拉取配置后，本地 `master` 分支应用的所有人工修改项。
在自动同步流程中，这些项由 `.github/scripts/customize_quantumultx.py` 动态注入，并在此后得到强制断言保护。

## 1. freeSub 备用节点
- **默认关闭**：`enabled=false`
- **目的**：仅在本地机场失效时作为手工干预的备用资源，平时不参与策略组路由，防止污染。

## 2. 自动测速配置
- **检查间隔**：从原版的 `check-interval=1200` 统一调整为 `check-interval=900`（15分钟），注释也一并修正。
- **容差**：保留 `tolerance=0` 设定。

## 3. 地区策略 Emoji 兼容
为满足本地部分含有国旗 Emoji 节点的机场，针对五个主干地区进行了精确正则替换。
既在包含中加入 Emoji，也在排除组（`(?!(...))`）中对称加入了 Emoji 以防止误匹配：
- 🇭🇰 香港：`(港|HK|(?i)Hong|🇭🇰)`
- 🇹🇼 台湾：`(台|TW|(?i)Taiwan|🇹🇼)`
- 🇯🇵 日本：`(日|JP|(?i)Japan|🇯🇵)`
- 🇸🇬 新加坡：`(新|狮|獅|SG|(?i)Singapore|🇸🇬)`
- 🇺🇸 美国：`(美|US|(?i)States|American|🇺🇸)`

## 4. 资源地址全部内网化 (hanhan-ggit)
避免受原作者封锁或删库影响，所有关键配置资源均替换为 `hanhan-ggit` 账户下的克隆库版本：
- `ddgksf2013/Filter` -> `hanhan-ggit/Filter`
- `ddgksf2013/Rewrite` -> `hanhan-ggit/Rewrite`
- `blackmatrix7/ios_rule_script` -> `hanhan-ggit/ios_rule_script`
- `KOP-XIAO/QuantumultX` -> `hanhan-ggit/QuantumultX`
- `resource-parser.js` -> `hanhan-ggit/QuantumultX`

## 5. 防爬防盗链特殊处理的脚本
上游 `ddgksf2013.top` 域名对以下脚本启用了防爬虫拦截。已通过专用 `sync-ddgksf.yml` 伪装 UA 下载到本地，主配置中的链接对应改为 `hanhan-ggit/Profile` 直链：
- `StartUpAds.conf`
- `zhihu.ads.js`
- `XiaoHongShuAds.conf`
- `bdpan.ads.js`
- `bdpan.unlock.js`
- `BiliBiliAdsLite.conf`

## 6. 其他额外追加项目
- 注入了 `Ai.yaml` 策略。
- 注入了 `server-info-pure.js` (节点纯净度详情) 的 task 配置。