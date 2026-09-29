import sys
import re

def customize():
    try:
        with open('QuantumultX.conf', 'r', encoding='utf-8') as f:
            conf = f.read()
    except Exception as e:
        print("Failed to read QuantumultX.conf:", e)
        sys.exit(1)

    # 1. freeSub -> enabled=false
    lines = conf.splitlines()
    for i, line in enumerate(lines):
        if 'freeSub' in line and 'enabled=true' in line:
            lines[i] = line.replace('enabled=true', 'enabled=false')
    conf = "\n".join(lines) + ("\n" if conf.endswith("\n") else "")

    # 2 & 3. check-interval=900 & tolerance=0
    new_lines = []
    for line in conf.splitlines():
        if line.startswith('url-latency-benchmark='):
            line = re.sub(r'check-interval=\d+', 'check-interval=900', line)
        elif line.startswith('#将下面的url-latency-benchmark'):
            line = re.sub(r'check-interval=\d+', 'check-interval=900', line)
        new_lines.append(line)
    conf = "\n".join(new_lines) + ("\n" if conf.endswith("\n") else "")

    # 4. Emoji
    replacements = [
        (r'\(港\|HK\|\(\?i\)Hong(\|🇭🇰)?\)', '(港|HK|(?i)Hong|🇭🇰)'),
        (r'\(台\|日\|韩\|新\|美(\|🇹🇼\|🇯🇵\|🇰🇷\|🇸🇬\|🇺🇸)?\)', '(台|日|韩|新|美|🇹🇼|🇯🇵|🇰🇷|🇸🇬|🇺🇸)'),
        (r'\(台\|TW\|\(\?i\)Taiwan(\|🇹🇼)?\)', '(台|TW|(?i)Taiwan|🇹🇼)'),
        (r'\(港\|日\|韩\|新\|美(\|🇭🇰\|🇯🇵\|🇰🇷\|🇸🇬\|🇺🇸)?\)', '(港|日|韩|新|美|🇭🇰|🇯🇵|🇰🇷|🇸🇬|🇺🇸)'),
        (r'\(日\|JP\|\(\?i\)Japan(\|🇯🇵)?\)', '(日|JP|(?i)Japan|🇯🇵)'),
        (r'\(港\|台\|韩\|新\|美(\|🇭🇰\|🇹🇼\|🇰🇷\|🇸🇬\|🇺🇸)?\)', '(港|台|韩|新|美|🇭🇰|🇹🇼|🇰🇷|🇸🇬|🇺🇸)'),
        (r'\(新\|狮\|獅\|SG\|\(\?i\)Singapore(\|🇸🇬)?\)', '(新|狮|獅|SG|(?i)Singapore|🇸🇬)'),
        (r'\(港\|台\|日\|韩\|美(\|🇭🇰\|🇹🇼\|🇯🇵\|🇰🇷\|🇺🇸)?\)', '(港|台|日|韩|美|🇭🇰|🇹🇼|🇯🇵|🇰🇷|🇺🇸)'),
        (r'\(美\|US\|\(\?i\)States\|American(\|🇺🇸)?\)', '(美|US|(?i)States|American|🇺🇸)'),
        (r'\(港\|台\|日\|韩\|新(\|🇭🇰\|🇹🇼\|🇯🇵\|🇰🇷\|🇸🇬)?\)', '(港|台|日|韩|新|🇭🇰|🇹🇼|🇯🇵|🇰🇷|🇸🇬)')
    ]
    for old, new in replacements:
        conf = re.sub(old, new, conf)

    # 5. hanhan-ggit Custom resources
    conf = conf.replace('ddgksf2013/Rewrite', 'hanhan-ggit/Rewrite')
    conf = conf.replace('ddgksf2013/Filter', 'hanhan-ggit/Filter')
    conf = conf.replace('blackmatrix7/ios_rule_script', 'hanhan-ggit/ios_rule_script')
    conf = conf.replace('KOP-XIAO/QuantumultX', 'hanhan-ggit/QuantumultX')

    # Replace ddgksf2013.top links
    ddgksf_links = [
        ('https://ddgksf2013.top/rewrite/StartUpAds.conf', 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/rewrite/StartUpAds.conf'),
        ('https://ddgksf2013.top/scripts/zhihu.ads.js', 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/scripts/zhihu.ads.js'),
        ('https://ddgksf2013.top/rewrite/XiaoHongShuAds.conf', 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/rewrite/XiaoHongShuAds.conf'),
        ('https://ddgksf2013.top/scripts/bdpan.ads.js', 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/scripts/bdpan.ads.js'),
        ('https://ddgksf2013.top/scripts/bdpan.unlock.js', 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/scripts/bdpan.unlock.js'),
        ('https://ddgksf2013.top/rewrite/BiliBiliAdsLite.conf', 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/rewrite/BiliBiliAdsLite.conf')
    ]
    for old, new in ddgksf_links:
        conf = conf.replace(old, new)
        old_raw = old.replace('https://ddgksf2013.top/', 'https://raw.githubusercontent.com/ddgksf2013/Profile/master/')
        conf = conf.replace(old_raw, new)

    # Re-inject missing hanhan-ggit exclusive scripts
    if 'Ai.yaml' not in conf and 'GoogleVoice.list' in conf:
        lines = conf.splitlines()
        for i, line in enumerate(lines):
            if 'GoogleVoice.list' in line:
                lines.insert(i+1, 'https://raw.githubusercontent.com/hanhan-ggit/Profile/master/filter/Ai.yaml, tag=Ai-All-In-One, img-url=https://raw.githubusercontent.com/ddgksf2013/Icon/master/qx/ai.png, force-policy=美国节点, update-interval=604800, opt-parser=true, enabled=true')
                break
        conf = "\n".join(lines) + ("\n" if conf.endswith("\n") else "")

    if 'server-info-pure.js' not in conf and 'streaming-ui-check.js' in conf:
        lines = conf.splitlines()
        for i, line in enumerate(lines):
            if 'streaming-ui-check.js' in line:
                lines.insert(i+1, 'event-interaction https://raw.githubusercontent.com/hanhan-ggit/Profile/master/scripts/server-info-pure.js, tag=节点纯净度详情, img-url=checkmark.shield.fill.system')
                break
        conf = "\n".join(lines) + ("\n" if conf.endswith("\n") else "")

    with open('QuantumultX.conf', 'w', encoding='utf-8') as f:
        f.write(conf)
        
    print("Customization applied successfully.")

if __name__ == '__main__':
    customize()