/**
 * Evolve 游戏自动化效率脚本 v2
 * =================================
 * 适用于: https://g8hh.github.io/evolve/ (进化 - Evolve)
 * 用法: 打开游戏页面后，F12 → Console，粘贴此脚本并回车
 *
 * v2 更新:
 *   - 修复 ES Module 导致 window.e 不可访问的问题
 *   - 通过 __vue__ / localStorage 读取游戏状态
 *   - 纯 DOM 交互，不依赖模块内部变量
 *   - 智能按钮识别，适配各个游戏阶段
 */

(function() {
    'use strict';

    // ==================== 配置 ====================
    const DEFAULT_CONFIG = {
        autoClick: true,
        autoBuild: true,
        autoResearch: true,
        autoJob: true,
        autoTrade: true,
        autoEvent: true,
        autoARPA: true,
        clickInterval: 100,
        buildInterval: 500,
        researchInterval: 1000,
        jobInterval: 2000,
        tradeInterval: 3000,
        eventInterval: 1000,
    };

    const config = { ...DEFAULT_CONFIG };
    let running = true;
    let gameStateAccess = 'none'; // 'vue' | 'localStorage' | 'none'
    let _vueRoot = null;
    let _cachedState = null;
    let _cacheTime = 0;

    let stats = { clicks:0, builds:0, researches:0, jobsAssigned:0, trades:0, eventsHandled:0, startTime:Date.now() };

    // ==================== 日志 ====================
    function log(msg, type='info') {
        const colors = { info:'#4fc3f7', success:'#66bb6a', warning:'#ffa726', error:'#ef5350', action:'#ab47bc' };
        console.log('%c[EvolveBot]%c ' + msg,
            `color:${colors[type]};font-weight:bold;`, 'color:inherit;');
    }

    // ==================== 游戏状态访问 ====================

    /** 尝试通过 Vue 实例获取游戏状态 */
    function findVueRoot() {
        if (_vueRoot) return _vueRoot;

        // 方法1: 扫描 DOM 树找 __vue__（Vue 2 会把实例挂到根元素上）
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_ELEMENT,
            {
                acceptNode: function(node) {
                    // 优先找有大量子元素的大容器（大概率是 Vue 根节点）
                    if (node.__vue__ && node.__vue__._data) return NodeFilter.FILTER_ACCEPT;
                    // Vue 2 Buefy 根元素
                    if (node.__vue__ && node.__vue__.$root) return NodeFilter.FILTER_ACCEPT;
                    return NodeFilter.FILTER_SKIP;
                }
            }
        );

        const candidates = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.__vue__) {
                const vm = node.__vue__;
                // 找最顶层的 Vue 实例（$root === vm）
                const root = vm.$root || vm;
                if (root._data || root.$data) {
                    candidates.push(root);
                }
            }
        }

        // 优先选 data 最大的（最可能是游戏根实例）
        if (candidates.length > 0) {
            candidates.sort((a, b) => {
                const aKeys = Object.keys(a._data || a.$data || {}).length;
                const bKeys = Object.keys(b._data || b.$data || {}).length;
                return bKeys - aKeys;
            });
            _vueRoot = candidates[0];
            return _vueRoot;
        }

        // 方法2: 暴力扫描所有元素的 __vue__
        const all = document.querySelectorAll('*');
        for (const el of all) {
            if (el.__vue__) {
                const vm = el.__vue__;
                const data = vm._data || vm.$data || {};
                const keys = Object.keys(data);
                // 游戏状态通常有很多 key
                if (keys.length > 20) {
                    _vueRoot = vm;
                    return _vueRoot;
                }
            }
        }

        return null;
    }

    /** 通过 Vue 实例读取游戏状态 */
    function getStateFromVue() {
        const root = findVueRoot();
        if (!root) return null;
        const data = root._data || root.$data || {};

        // Vue 2 的数据可能在 data 或直接挂在实例上
        // 找包含 resource/race/tech 的对象
        for (const key of Object.keys(data)) {
            const val = data[key];
            if (val && typeof val === 'object' && val.resource && val.race) {
                return val;
            }
        }
        // 也可能整个 data 就是游戏状态
        if (data.resource && data.race) return data;
        return null;
    }

    /** 通过 localStorage 读取游戏状态 */
    function getStateFromStorage() {
        try {
            const raw = localStorage.getItem('evolved');
            if (!raw) return null;
            const decompressed = LZString.decompressFromUTF16(raw);
            if (!decompressed) return null;
            return JSON.parse(decompressed);
        } catch (e) {
            return null;
        }
    }

    /** 综合获取游戏状态（带缓存，1秒内不重复读取） */
    function getGameState() {
        const now = Date.now();
        if (_cachedState && now - _cacheTime < 1000) return _cachedState;

        // 优先从 Vue 实例读取（实时数据）
        let state = getStateFromVue();
        if (state) {
            gameStateAccess = 'vue';
            _cachedState = state;
            _cacheTime = now;
            return state;
        }

        // 回退到 localStorage（可能有延迟）
        state = getStateFromStorage();
        if (state) {
            gameStateAccess = 'localStorage';
            _cachedState = state;
            _cacheTime = now;
            return state;
        }

        gameStateAccess = 'none';
        return null;
    }

    /** 等待游戏加载完成 */
    function waitForGame(timeout = 15000) {
        const start = Date.now();
        return new Promise((resolve, reject) => {
            const check = () => {
                const elapsed = Date.now() - start;

                // 方法1: 检查 Vue 实例
                if (getStateFromVue() || getStateFromStorage()) {
                    resolve(getGameState());
                    return;
                }

                // 方法2: 检查 DOM 是否已有游戏元素
                const buttons = document.querySelectorAll('button.button:not(#evolve-bot-panel button), [role="button"]');
                if (buttons.length > 5) {
                    resolve(getGameState());
                    return;
                }

                if (elapsed > timeout) {
                    reject(new Error('超时：未检测到游戏，请在 https://g8hh.github.io/evolve/ 页面运行'));
                    return;
                }

                setTimeout(check, 200);
            };
            check();
        });
    }

    // ==================== 智能按钮查找 ====================

    /** 判断一个元素是否真正可见 */
    function isVisible(el) {
        if (!el || !el.offsetParent) return false;
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
    }

    /** 判断按钮是否可用（不是灰色/禁用） */
    function isButtonAvailable(btn) {
        if (!isVisible(btn)) return false;
        if (btn.hasAttribute('disabled') && btn.getAttribute('disabled') !== 'false') return false;
        if (btn.classList.contains('has-text-fade')) return false;
        if (btn.classList.contains('is-static')) return false;
        // Buefy 用 disabled 属性
        if (btn.disabled) return false;
        return true;
    }

    /** 查找当前阶段主要操作按钮 */
    function findMainActionButton() {
        // 策略：找页面中最「醒目」的按钮
        // 游戏通常有一个大的、带颜色的主要操作按钮

        const allButtons = document.querySelectorAll('button, [role="button"]');
        const candidates = [];

        for (const btn of allButtons) {
            if (!isButtonAvailable(btn)) continue;
            // 排除控制面板、消息队列、导航栏
            if (btn.closest('#evolve-bot-panel')) continue;
            if (btn.closest('#msgQueue')) continue;
            if (btn.closest('.navbar') || btn.closest('nav')) continue;

            const text = (btn.textContent || '').toLowerCase();
            const cls = btn.className || '';

            // 计算「醒目度」分数
            let score = 0;

            // 进化/收集关键词
            if (/进化|evolv|collect|gather|click|harvest|mine|farm|hunt|grab|catch/i.test(text)) score += 30;
            // 醒目样式
            if (/is-warning|is-primary|is-success|has-text-warning|has-text-primary/i.test(cls)) score += 20;
            // 大按钮
            if (btn.offsetWidth > 80 && btn.offsetHeight > 30) score += 10;
            // 不是小图标按钮
            if (btn.offsetWidth > 40) score += 5;
            // 不在侧边栏
            if (!btn.closest('.sidebar') && !btn.closest('aside')) score += 5;
            // 不包含数字（纯操作按钮，非购买按钮）
            if (!/\d/.test(text.trim())) score += 5;

            if (score > 0) candidates.push({ btn, score });
        }

        candidates.sort((a, b) => b.score - a.score);
        return candidates.length > 0 ? candidates[0].btn : null;
    }

    /** 查找当前标签页中可用的购买按钮 */
    function findBuyButtons() {
        const buttons = [];
        const all = document.querySelectorAll('button.button:not(.has-text-fade):not([disabled]), [role="button"]:not(.has-text-fade)');

        for (const btn of all) {
            if (!isButtonAvailable(btn)) continue;
            if (btn.closest('#evolve-bot-panel')) continue;
            if (btn.closest('#msgQueue')) continue;

            const text = (btn.textContent || '').trim();
            const parentText = (btn.parentElement?.textContent || '').trim();

            // 购买按钮特征：
            // 1. 包含数字和资源名
            // 2. 包含 "Build"/"建造"/"Buy"/"购买" 等文字
            // 3. 在建造队列或建筑区域中
            const isBuyBtn = (
                /\d/.test(text) ||                                    // 包含数量
                /build|buy|construct|upgrade|hire|train|research/i.test(text) ||
                /建造|购买|升级|雇佣|训练|研究|招募/i.test(text) ||
                btn.closest('#buildQueue') ||
                btn.closest('#queue') ||
                btn.closest('.build-queue')
            );

            if (isBuyBtn) {
                buttons.push(btn);
            }
        }

        // 按性价比排序：文字越短越基础（通常越便宜）
        buttons.sort((a, b) => {
            const aLen = (a.getAttribute('aria-label') || a.textContent || '').length;
            const bLen = (b.getAttribute('aria-label') || b.textContent || '').length;
            return aLen - bLen;
        });

        return buttons;
    }

    /** 查找研究按钮 */
    function findResearchButtons() {
        const buttons = [];
        // 常见的研究区域
        const areas = ['#research', '#techTree', '#tech', '.research', '.science',
                       '[class*="research"]', '[class*="tech"]'];
        const containers = [];

        for (const sel of areas) {
            const el = document.querySelector(sel);
            if (el) containers.push(el);
        }

        // 如果没找到特定区域，扫描全页
        const searchIn = containers.length > 0 ? containers : [document.body];

        for (const container of searchIn) {
            const btns = container.querySelectorAll('button.button:not(.has-text-fade):not([disabled]), [role="button"]:not(.has-text-fade)');
            for (const btn of btns) {
                if (!isButtonAvailable(btn)) continue;
                if (btn.closest('#evolve-bot-panel')) continue;
                if (btn.closest('#msgQueue')) continue;

                const text = (btn.textContent || '').toLowerCase();
                const label = (btn.getAttribute('aria-label') || '').toLowerCase();

                // 研究按钮特征
                if (/research|study|discover|invent|learn/i.test(text + label)) {
                    buttons.push(btn);
                    continue;
                }
                if (/研究|学习|发现|发明/i.test(text + label)) {
                    buttons.push(btn);
                    continue;
                }
                // ARPA 项目按钮
                if (btn.closest('#arpa') || btn.closest('.arpaProject')) {
                    if (btn.classList.contains('gbuy') || /\d/.test(text)) {
                        buttons.push(btn);
                    }
                }
            }
        }

        return buttons;
    }

    /** 查找工作分配按钮 */
    function findJobButtons() {
        const buttons = [];
        // Civic/工作面板
        const civicAreas = document.querySelectorAll('#civic, #civics, [class*="civic"], #jobs, #workers');
        for (const area of civicAreas) {
            const btns = area.querySelectorAll('[role="button"]:not(.has-text-fade), button:not(.has-text-fade)');
            for (const btn of btns) {
                if (!isButtonAvailable(btn)) continue;
                const label = (btn.getAttribute('aria-label') || btn.textContent || '');
                // 添加工人按钮
                if (/\+|add|hire|雇|加|分配|assign/i.test(label)) {
                    buttons.push(btn);
                }
            }
        }
        return buttons;
    }

    // ==================== 自动化操作 ====================

    function doAutoClick() {
        if (!config.autoClick || !running) return;
        const btn = findMainActionButton();
        if (btn) {
            // 同时触发原生 click 和 Vue 的 @click
            btn.click();
            btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
            btn.dispatchEvent(new Event('change', { bubbles: true }));
            stats.clicks++;
        }
    }

    function doAutoBuild() {
        if (!config.autoBuild || !running) return;
        const buttons = findBuyButtons();
        if (buttons.length > 0) {
            buttons[0].click();
            stats.builds++;
            return;
        }
        // 回退：买任何看起来可买的
        const anyBtn = document.querySelector('button.button:not(.has-text-fade):not([disabled]):not(.is-static)');
        if (anyBtn && isVisible(anyBtn) && !anyBtn.closest('#evolve-bot-panel') && !anyBtn.closest('#msgQueue')) {
            anyBtn.click();
            stats.builds++;
        }
    }

    function doAutoResearch() {
        if (!config.autoResearch || !running) return;
        const buttons = findResearchButtons();
        if (buttons.length > 0) {
            buttons[0].click();
            stats.researches++;
        }
    }

    function doAutoJob() {
        if (!config.autoJob || !running) return;
        const buttons = findJobButtons();
        if (buttons.length > 0) {
            buttons[0].click();
            stats.jobsAssigned++;
        }
    }

    function doAutoTrade() {
        if (!config.autoTrade || !running) return;
        // 找卖资源的按钮
        const marketBtns = document.querySelectorAll('#market button:not(.has-text-fade), #trade button:not(.has-text-fade)');
        for (const btn of marketBtns) {
            if (!isButtonAvailable(btn)) continue;
            const label = (btn.getAttribute('aria-label') || btn.textContent || '').toLowerCase();
            if (/sell|卖|出售|trade/i.test(label)) {
                btn.click();
                stats.trades++;
                break;
            }
        }
    }

    function doAutoEvent() {
        if (!config.autoEvent || !running) return;
        // 弹窗/模态框
        const modals = document.querySelectorAll('.modal.is-active, .notification, .dialog, [class*="event"]');
        for (const modal of modals) {
            if (!isVisible(modal)) continue;
            const confirmBtn = modal.querySelector('button.is-success, button.is-primary, .button:not(.is-danger):not(.has-text-fade)');
            if (confirmBtn && isVisible(confirmBtn)) {
                confirmBtn.click();
                stats.eventsHandled++;
                return;
            }
        }
        // 消息队列按钮
        const msgBtns = document.querySelectorAll('#msgQueue button.button:not(.has-text-fade)');
        for (const btn of msgBtns) {
            if (isVisible(btn)) {
                btn.click();
                stats.eventsHandled++;
            }
        }
    }

    function doAutoARPA() {
        if (!config.autoARPA || !running) return;
        const arpaSection = document.querySelector('#arpa');
        if (!arpaSection) return;
        const btns = arpaSection.querySelectorAll('button.button:not(.has-text-fade):not([disabled]), .gbuy:not(.has-text-fade)');
        for (const btn of btns) {
            if (isButtonAvailable(btn)) {
                btn.click();
                break;
            }
        }
    }

    // ==================== 控制面板 ====================

    function createPanel() {
        const existing = document.getElementById('evolve-bot-panel');
        if (existing) existing.remove();

        const panel = document.createElement('div');
        panel.id = 'evolve-bot-panel';
        panel.innerHTML = `
<style>
#evolve-bot-panel{position:fixed;top:10px;right:10px;z-index:99999;background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #0f3460;border-radius:12px;padding:15px;color:#e0e0e0;font-family:'Segoe UI',system-ui,sans-serif;font-size:13px;min-width:260px;max-width:300px;box-shadow:0 8px 32px rgba(0,0,0,0.5);user-select:none;}
#evolve-bot-panel.minimized .bot-content{display:none;}
#evolve-bot-panel.minimized{min-width:auto;}
#evolve-bot-panel h3{margin:0 0 10px 0;font-size:16px;color:#4fc3f7;cursor:pointer;display:flex;justify-content:space-between;align-items:center;}
#evolve-bot-panel .bot-row{display:flex;justify-content:space-between;align-items:center;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.05);}
#evolve-bot-panel label{cursor:pointer;flex:1;color:#e0e0e0;}
#evolve-bot-panel input[type="checkbox"]{margin-right:8px;cursor:pointer;accent-color:#4fc3f7;}
#evolve-bot-panel input[type="range"]{width:100%;margin:4px 0;accent-color:#4fc3f7;}
#evolve-bot-panel .btn-group{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;}
#evolve-bot-panel button{background:#0f3460;color:#e0e0e0;border:1px solid #1a5276;border-radius:6px;padding:5px 12px;cursor:pointer;font-size:12px;transition:all 0.2s;}
#evolve-bot-panel button:hover{background:#1a5276;}
#evolve-bot-panel button.active{background:#27ae60;border-color:#2ecc71;}
#evolve-bot-panel button.danger{background:#c0392b;border-color:#e74c3c;}
#evolve-bot-panel button.danger:hover{background:#e74c3c;}
#evolve-bot-panel .stats{font-size:11px;color:#888;margin-top:8px;line-height:1.5;}
#evolve-bot-panel .stats span{color:#4fc3f7;}
</style>
<h3>🤖 EvolveBot <span class="toggle-icon" id="bot-toggle">▼</span></h3>
<div class="bot-content">
    <div class="bot-row">
        <label><input type="checkbox" id="bot-autoClick" checked> 自动点击</label>
        <span style="color:#888;font-size:11px" id="bot-speed-label">100ms</span>
    </div>
    <div class="bot-row"><label><input type="checkbox" id="bot-autoBuild" checked> 自动建造</label></div>
    <div class="bot-row"><label><input type="checkbox" id="bot-autoResearch" checked> 自动研究</label></div>
    <div class="bot-row"><label><input type="checkbox" id="bot-autoJob" checked> 自动分配工作</label></div>
    <div class="bot-row"><label><input type="checkbox" id="bot-autoTrade" checked> 自动交易</label></div>
    <div class="bot-row"><label><input type="checkbox" id="bot-autoEvent" checked> 自动处理事件</label></div>
    <div class="bot-row"><label><input type="checkbox" id="bot-autoARPA" checked> 自动 ARPA</label></div>
    <div style="margin-top:6px">
        <span style="font-size:11px;color:#888">点击速度: 快 ← → 慢</span>
        <input type="range" id="bot-speed" min="50" max="1000" value="100" step="10">
    </div>
    <div class="btn-group">
        <button id="bot-pause">⏸ 暂停</button>
        <button id="bot-export">📋 导出存档</button>
        <button id="bot-reset-stats">🔄 重置统计</button>
        <button id="bot-close" class="danger">✕ 关闭</button>
    </div>
    <div class="stats" id="bot-stats-text">
        状态访问: <span id="bot-access">检测中...</span><br>
        运行时间: <span id="bot-runtime">0s</span><br>
        点击:<span id="bot-clicks">0</span> 建造:<span id="bot-builds">0</span> 研究:<span id="bot-researches">0</span><br>
        工作:<span id="bot-jobs">0</span> 交易:<span id="bot-trades">0</span> 事件:<span id="bot-events">0</span>
    </div>
</div>`;
        document.body.appendChild(panel);
        bindPanelEvents();
    }

    function bindPanelEvents() {
        document.getElementById('bot-toggle').onclick = () => {
            document.getElementById('evolve-bot-panel').classList.toggle('minimized');
        };

        const map = {
            'bot-autoClick':'autoClick','bot-autoBuild':'autoBuild',
            'bot-autoResearch':'autoResearch','bot-autoJob':'autoJob',
            'bot-autoTrade':'autoTrade','bot-autoEvent':'autoEvent',
            'bot-autoARPA':'autoARPA'
        };
        Object.entries(map).forEach(([id, key]) => {
            document.getElementById(id).onchange = (e) => { config[key] = e.target.checked; };
        });

        document.getElementById('bot-speed').oninput = (e) => {
            config.clickInterval = parseInt(e.target.value);
            document.getElementById('bot-speed-label').textContent = e.target.value + 'ms';
            restartClickTimer();
        };

        document.getElementById('bot-pause').onclick = function() {
            running = !running;
            this.textContent = running ? '⏸ 暂停' : '▶ 继续';
            this.classList.toggle('active', !running);
            if (running) { startAll(); log('已恢复运行', 'success'); }
            else { log('已暂停', 'warning'); }
        };

        document.getElementById('bot-export').onclick = () => {
            try {
                if (typeof window.exportGame === 'function') {
                    const save = window.exportGame();
                    navigator.clipboard.writeText(save).then(() => log('存档已复制到剪贴板！', 'success'));
                } else {
                    // 直接读 localStorage
                    const raw = localStorage.getItem('evolved');
                    if (raw) {
                        navigator.clipboard.writeText(raw).then(() => log('存档已复制到剪贴板！', 'success'));
                    } else {
                        log('无法读取存档', 'error');
                    }
                }
            } catch(e) {
                log('导出失败: ' + e.message, 'error');
            }
        };

        document.getElementById('bot-reset-stats').onclick = () => {
            stats = { clicks:0, builds:0, researches:0, jobsAssigned:0, trades:0, eventsHandled:0, startTime:Date.now() };
            updateStatsDisplay();
            log('统计已重置', 'info');
        };

        document.getElementById('bot-close').onclick = () => {
            stopAll();
            document.getElementById('evolve-bot-panel').remove();
            log('脚本已关闭，刷新页面可重新启动', 'warning');
        };
    }

    function updateStatsDisplay() {
        const runtime = Math.floor((Date.now() - stats.startTime) / 1000);
        const h = Math.floor(runtime / 3600), m = Math.floor((runtime % 3600) / 60), s = runtime % 60;
        const timeStr = h>0 ? `${h}h${m}m${s}s` : m>0 ? `${m}m${s}s` : `${s}s`;
        const set = (id, v) => { const el = document.getElementById(id); if(el) el.textContent = v; };
        set('bot-runtime', timeStr);
        set('bot-clicks', stats.clicks.toLocaleString());
        set('bot-builds', stats.builds.toLocaleString());
        set('bot-researches', stats.researches.toLocaleString());
        set('bot-jobs', stats.jobsAssigned.toLocaleString());
        set('bot-trades', stats.trades.toLocaleString());
        set('bot-events', stats.eventsHandled.toLocaleString());
        set('bot-access', gameStateAccess === 'vue' ? '✅ Vue 实时' : gameStateAccess === 'localStorage' ? '⚠️ 存档读取' : '❌ 纯DOM');
    }

    // ==================== 定时器 ====================

    let clickTimer, buildTimer, researchTimer, jobTimer, tradeTimer, eventTimer, arpaTimer, statsTimer;

    function restartClickTimer() {
        if (clickTimer) clearInterval(clickTimer);
        if (config.autoClick) clickTimer = setInterval(doAutoClick, config.clickInterval);
    }

    function startAll() {
        stopAll();
        if (!running) return;
        restartClickTimer();
        buildTimer = setInterval(doAutoBuild, config.buildInterval);
        researchTimer = setInterval(doAutoResearch, config.researchInterval);
        jobTimer = setInterval(doAutoJob, config.jobInterval);
        tradeTimer = setInterval(doAutoTrade, config.tradeInterval);
        eventTimer = setInterval(doAutoEvent, config.eventInterval);
        arpaTimer = setInterval(doAutoARPA, config.researchInterval + 500);
        statsTimer = setInterval(updateStatsDisplay, 1000);
    }

    function stopAll() {
        [clickTimer,buildTimer,researchTimer,jobTimer,tradeTimer,eventTimer,arpaTimer,statsTimer].forEach(t => {
            if (t) clearInterval(t);
        });
        clickTimer=buildTimer=researchTimer=jobTimer=tradeTimer=eventTimer=arpaTimer=statsTimer=null;
    }

    // ==================== 初始化 ====================

    async function init() {
        log('EvolveBot v2 初始化中...', 'info');

        try {
            await waitForGame();
            const state = getGameState();
            if (state) {
                const species = state.race?.species || '未知';
                const universe = state.race?.universe || 'standard';
                const resCount = Object.keys(state.resource || {}).length;
                log(`已连接游戏 (${gameStateAccess})`, 'success');
                log(`物种: ${species} | 宇宙: ${universe} | 资源数: ${resCount}`, 'info');
            } else {
                log('游戏状态读取受限，将使用纯 DOM 模式运行', 'warning');
            }
        } catch (err) {
            log(err.message, 'error');
            log('尝试纯 DOM 模式启动...', 'warning');
        }

        createPanel();
        startAll();
        updateStatsDisplay();

        log('🚀 EvolveBot v2 已启动！', 'success');
        log('💡 面板在右上角 | Ctrl+Shift+B 暂停 | Ctrl+Shift+E 紧急停止', 'info');

        window.__evolveBot = {
            config, stats, get running() { return running; },
            start: startAll, stop: stopAll, getState: getGameState,
            destroy() { stopAll(); const p=document.getElementById('evolve-bot-panel'); if(p)p.remove(); delete window.__evolveBot; }
        };
    }

    init().catch(err => { log('初始化失败: '+err.message, 'error'); console.error(err); });

    // ==================== 快捷键 ====================
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey) {
            if (e.key.toLowerCase() === 'b') {
                e.preventDefault();
                running = !running;
                const btn = document.getElementById('bot-pause');
                if (btn) { btn.textContent = running ? '⏸ 暂停' : '▶ 继续'; btn.classList.toggle('active', !running); }
                if (running) startAll(); else stopAll();
                log(running ? '已恢复运行' : '已暂停', running ? 'success' : 'warning');
            } else if (e.key.toLowerCase() === 'e') {
                e.preventDefault();
                stopAll(); running = false;
                const btn = document.getElementById('bot-pause');
                if (btn) { btn.textContent = '▶ 继续'; btn.classList.add('active'); }
                log('🛑 紧急停止！', 'error');
            }
        }
    });

})();
