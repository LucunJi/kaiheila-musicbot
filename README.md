# Kaiheila Musicbot（开黑啦音乐 bot）

## 简介/Intro

这个 bot 可以在开黑啦的语音频道中播放音乐。

**使用之前请先根据 设置 这一小节进行配置**

使用了 selenium + docker + 

未完工。

## 设置/Config

复制一份 `selenium_bot/botcfg-template.json` 并改名为 `botcfg.json`（文件位置不变）。以下是各条参数的填写指南。编辑时请自行搜索并参照 JSON 规范。

- region: 手机区号，例如：`+86`
- phone：手机号码
- password：密码
- server_id：服务器的 id，可以在网址里找到，格式为：`https://www.kaiheila.cn/app/channels/<server_id>`
- channel_name：频道名字
- selenium_additional_args：selenium 启动 Chrome 浏览器时可以使用的默认参数。**请不要在不知道确切用途的情况下改动已有的参数**

## 引用/Credits

整体架构：https://superuser.com/questions/1223118/emulating-microphone-input-to-chrome-inside-docker-container
