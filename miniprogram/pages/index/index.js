// pages/index/index.js — 主聊天页面
const api = require('../../utils/api');

Page({
  data: {
    messages: [],
    inputValue: '',
    scrollToView: '',
    loading: false,
  },

  onLoad() {
    // 初始欢迎消息
    this.addMessage('assistant', '你好！我是周末搭子 🎉\n告诉我你想在哪个城市玩？和谁一起？有什么特殊需求吗？');
  },

  // 输入框绑定
  onInput(e) {
    this.setData({ inputValue: e.detail.value });
  },

  // 发送消息
  async onSend() {
    const message = this.data.inputValue.trim();
    if (!message || this.data.loading) return;

    this.addMessage('user', message);
    this.setData({ inputValue: '', loading: true });

    try {
      const res = await api.sendChatMessage(message);
      if (res.plans && res.plans.length > 0) {
        this.addMessage('assistant', '为您找到以下方案：');
        // 添加方案卡片到消息流
        res.plans.forEach(plan => {
          this.addMessage('plan_card', plan);
        });
      } else if (res.reply) {
        this.addMessage('assistant', res.reply);
      }
    } catch (err) {
      this.addMessage('assistant', '网络出了点问题，请稍后重试 😅');
      console.error('Chat error:', err);
    }

    this.setData({ loading: false });
  },

  // 添加消息到列表
  addMessage(role, content) {
    const messages = this.data.messages;
    const id = 'msg-' + messages.length;
    messages.push({ id, role, content, time: new Date().toLocaleTimeString() });
    this.setData({ messages, scrollToView: id });
  },

  // 点击方案卡片
  onPlanTap(e) {
    const planId = e.currentTarget.dataset.planId;
    wx.navigateTo({
      url: '/pages/plan-detail/plan-detail?id=' + planId,
    });
  },
});
