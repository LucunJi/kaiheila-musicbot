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
- [x] 把设置选项全部移入环境变量，增加安全性
- [ ] 使用语音频道邀请链接替代服务器id和频道名称
- [ ] bot 被移动到别的语音频道后重新按下语音按键
- [ ] 可以接受来自另一个文字频道的用户指令，进行基本的播放/暂停/音量操作
- [ ] 点歌功能
- [ ] 多平台点歌功能

## 设置/Config

将 `.env.template` 和 `botcfg.env.template` 各复制一份并去除 `.template` 后缀。按照文件注释填写。

一般来说只需要修改 `botcfg.env` 就行了。

## 引用/Credits

整体架构参考了：https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container

pactl 的调教参考了：https://askubuntu.com/questions/1338747/virtual-audio-sink-virtual-audio-cable-on-ubuntu

Selenium Chrome 与 headless 相关的设置（懒得到处翻文档了）：https://stackoverflow.com/questions/53657215/running-selenium-with-headless-chrome-webdriver
