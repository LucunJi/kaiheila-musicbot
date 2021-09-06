# Kaiheila Musicbot（开黑啦音乐 bot）

## 简介/Intro

这个 bot 可以在开黑啦的语音频道中播放音乐。

**使用之前请先根据 设置 这一小节进行配置**

使用 Selenium + Docker + PulseAudio 实现自动登录，进入频道并输出音乐

### 目前进度：

未完工。

- [x] bot 登录、进入语音频道并按下语音按键
- [x] 使用 pactl 将音频输出重定向至输入播放声音
- [x] 关闭开黑啦语音设置里的所有语音改善选项，提高音质
- [x] 将 Python 脚本，Selenium 和 pactl 初始化脚本打包进 Docker 镜像， 提升可移植性并减少对主机的魔改
- [ ] 把设置选项全部移入环境变量，增加安全性
- [ ] 使用语音频道邀请链接替代服务器id和频道名称
- [ ] 可以接受来自另一个文字频道的用户指令，进行基本的播放/暂停/音量操作
- [ ] 点歌功能
- [ ] 多平台点歌功能

## 设置/Config

复制一份 `selenium_bot/botcfg-template.json` 并改名为 `botcfg.json`（文件位置不变）。以下是各条参数的填写指南。编辑时请自行搜索并参照 JSON 规范。

- region: 手机区号，最前面不要加号，例如：`86`
- phone：手机号码
- password：密码
- server_id：服务器的 id，可以在网址里找到，格式为：`https://www.kaiheila.cn/app/channels/<server_id>`
- channel_name：频道名字
- selenium_additional_args：selenium 启动 Chrome 浏览器时可以使用的默认参数。**请不要在不知道确切用途的情况下改动已有的参数**

## 引用/Credits

整体架构参考了：https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container
pactl 的调教参考了：https://askubuntu.com/questions/1338747/virtual-audio-sink-virtual-audio-cable-on-ubuntu
Selenium Chrome 与 headless 相关的设置（懒得到处翻文档了）：https://stackoverflow.com/questions/53657215/running-selenium-with-headless-chrome-webdriver
