# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

单一 HTML 文件的倒计时器（countdown timer），双击 `timer.html` 在浏览器中打开即可使用，无需构建或安装依赖。

## Code Architecture

整个应用在一个 `timer.html` 中，分为三部分：

- **CSS**：`<style>` 块，深色主题，使用 CSS 自定义属性集中管理颜色（`--bg`, `--accent`, `--danger`, `--warning` 等）
- **HTML**：主 UI 结构，包括时间输入、圆形 SVG 进度环、控制按钮（开始/暂停/重置）、预设按钮
- **JS**：`<script>` 中 IIFE 包裹的逻辑

### JS 关键模块

| 函数 | 职责 |
|---|---|
| `setUI(mode)` | 统一管理按钮/输入框状态（idle/running/paused/expired） |
| `updateDisplay()` | 更新屏幕显示 + SVG 进度环 + 颜色阈值切换 |
| `startTimer()` | 启动 setInterval，每秒 tick |
| `pauseTimer()` | 暂停计时 |
| `handleTimerComplete()` | 到期处理：播放闹铃 + 通知 |
| `setTotal(t)` | 设置总时长并重置 UI |

### 闹铃系统

- `AudioContext` 惰性初始化，仅在首次触发闹铃时创建
- `beep(freq, duration)` 用 Web Audio API 生成单音，结束后自动 `disconnect()`
- `playAlarm()` 编排 4 声蜂鸣序列

### 关键约定

- SVG 进度环的周长由 JS 根据半径计算（`2 * PI * r`），避免 CSS/JS 双端维护硬编码值
- 进度颜色使用 `lastClass` 状态跟踪，仅在跨越阈值时变更 DOM，避免每秒空操作
- 常量提取到顶部：`DEFAULT_SECONDS`, `TICK_MS`, `WARNING_RATIO`, `DANGER_RATIO` 等
- 键盘快捷键：空格 = 开始/暂停，R = 重置
- `beforeunload` 事件清理 timer 和 AudioContext，防止资源泄漏
