---
layout: page
title: 關於我 | About Me
permalink: /about/
---

<div class="about-container">
  <div class="about-header">
    <h2 class="about-name">黃苙凱 (Ray Huang)</h2>
    <p class="about-tagline">國立海洋大學 通訊與導航學系 | AI & 邊緣運算 / FRC 機器人電控與程式</p>
  </div>

  <hr>

  <p class="about-intro">
    對科技與動手實作充滿熱情，具備 **Arduino 開發、機電整合與 AIoT 應用** 經驗。曾參與 FRC 國際機器人競賽並負責視覺辨識與 PID 控制整合，擅長跨領域問題解決。工作與學習之餘熱愛 **攝影** 與 **品味咖啡**，也喜歡打桌球、健身和桌遊。
  </p>

  <div class="about-section">
    <h3>🏆 競賽經歷 (Competition Experience)</h3>
    <ul class="experience-list">
      <li><strong>2023</strong> | FRC 機器人夏威夷區域賽 & 新北區域大賽</li>
      <li><strong>2023</strong> | 公共運輸再進化 NetZero 解題競賽</li>
      <li><strong>2022</strong> | 全國高級中學生活科技學藝競賽 (創意設計組)</li>
      <li><strong>2021 - 2022</strong> | MAKEX 世界機器人挑戰賽</li>
    </ul>
  </div>

  <div class="about-section">
    <h3>💡 特殊事蹟 (Highlights)</h3>
    <ul class="highlights-list">
      <li><strong>FRC 團隊程式及電控講師</strong> (2022 - 2024)：負責新手培訓營隊之控制與電控教學。</li>
      <li><strong>FRC 區域賽志工 Control System Advisor (CSA)</strong> (2025)：協助賽事中各隊控制系統除錯與維護。</li>
      <li><strong>生活科技競賽教師研習助教</strong> (110 學年度)：協助藍牙晶片之使用與接線教學。</li>
    </ul>
  </div>

  <div class="about-grid">
    <div class="grid-card">
      <h3>💻 核心技能 (Skills)</h3>
      <p><strong>程式語言：</strong> Java, C++, Python, Verilog</p>
      <p><strong>硬體平台：</strong> roboRIO, Jetson Nano, Raspberry Pi, Arduino</p>
      <p><strong>領域技術：</strong> 邊緣運算 (AMB82_mini), 大語言模型 (Gemini / Llama) 微調與整合</p>
    </div>

    <div class="grid-card">
      <h3>☕ 興趣愛好 (Hobbies)</h3>
      <p>攝影 (Photography) ‧ 咖啡 (Coffee) ‧ 打桌球 ‧ 游泳 ‧ 桌遊 ‧ 跟 AI 聊天</p>
    </div>
  </div>

  <div class="about-section" style="margin-top: 2.5em; text-align: center;">
    <p>📧 聯絡郵件：<a href="mailto:moray.huang@gmail.com">moray.huang@gmail.com</a> | <a href="https://github.com/Li-Kai-Huang" target="_blank"><i class="fab fa-github"></i> GitHub</a></p>
  </div>
</div>

<style>
.about-container {
  line-height: 1.7;
}
.about-name {
  font-family: var(--brand-title-font);
  font-size: 2.2em;
  font-weight: 700;
  margin-bottom: 0.1em;
  color: var(--heading-color);
}
.about-tagline {
  font-size: 1.1em;
  color: var(--body-color-light);
  margin-top: 0;
  font-weight: 400;
}
.about-intro {
  font-size: 1.1em;
  margin: 1.5em 0;
}
.about-section {
  margin-top: 2em;
}
.about-section h3 {
  border-left: 4px solid var(--link-color);
  padding-left: 0.5em;
  margin-bottom: 0.8em;
}
.experience-list, .highlights-list {
  padding-left: 1.2em;
}
.experience-list li, .highlights-list li {
  margin-bottom: 0.6em;
}
.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5em;
  margin-top: 2em;
}
.grid-card {
  background-color: var(--body-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.2em;
  box-shadow: 0 2px 4px rgba(0,0,0,0.01);
}
.grid-card h3 {
  margin-top: 0;
  color: var(--link-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.4em;
  font-size: 1.15em;
  border-left: none;
  padding-left: 0;
}
@media (prefers-color-scheme: dark) {
  .grid-card {
    background-color: rgba(30, 41, 59, 0.3);
  }
}
</style>
