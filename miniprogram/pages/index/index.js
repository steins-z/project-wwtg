// pages/index/index.js — 主聊天页面
const api = require('../../utils/api');

Page({
  data: {
    messages: [],
    inputValue: '',
    scrollToView: '',
    loading: false,
    loadingText: '思考中...',
    sessionId: null,
  },

  onLoad() {
    this.addMessage('assistant', '你好！我是周末搭子 🎉\n告诉我你想在哪个城市玩？和谁一起？有什么特殊需求吗？');
  },

  onInput(e) {
    this.setData({ inputValue: e.detail.value });
  },

  async onSend() {
    const message = this.data.inputValue.trim();
    if (!message || this.data.loading) return;

    this.addMessage('user', message);
    this.setData({ inputValue: '', loading: true, loadingText: '正在了解你的需求...' });

    try {
      const app = getApp();
      if (app.globalData.mockMode) {
        const res = await api.sendChatMessage(message);
        this._handleResponse(res);
      } else {
        // Real API call
        this.setData({ loadingText: '正在了解你的需求...' });
        const res = await api.sendChatMessage(message);

        if (res.session_id) {
          this.setData({ sessionId: res.session_id });
          app.globalData.sessionId = res.session_id;
        }

        this._handleResponse(res);
      }
    } catch (err) {
      this.addMessage('assistant', '网络出了点问题，请稍后重试 😅');
      console.error('Chat error:', err);
    }

    this.setData({ loading: false });
  },

  _handleResponse(res) {
    if (res.plans && res.plans.length > 0) {
      this.addMessage('assistant', res.reply || '为您找到以下方案：');
      res.plans.forEach((plan, index) => {
        this.addMessage('plan_card', plan);
      });
      // Add action buttons
      this.addMessage('actions', {
        options: [
          { key: 'select_a', label: '就选A' },
          { key: 'select_b', label: '就选B' },
          { key: 'reject', label: '都不喜欢，换一批' },
        ]
      });
    } else if (res.reply) {
      this.addMessage('assistant', res.reply);
    }
  },

  addMessage(role, content) {
    const messages = this.data.messages;
    const id = 'msg-' + messages.length;
    messages.push({ id, role, content, time: new Date().toLocaleTimeString() });
    this.setData({ messages, scrollToView: id });
  },

  onPlanTap(e) {
    const planId = e.currentTarget.dataset.planId || (e.detail && e.detail.planId);
    if (planId) {
      wx.navigateTo({
        url: '/pages/plan-detail/plan-detail?id=' + planId,
      });
    }
  },

  onActionTap(e) {
    const action = e.currentTarget.dataset.action;
    if (action === 'select_a' || action === 'select_b') {
      this.addMessage('user', action === 'select_a' ? '就选A' : '就选B');
      this.setData({ loading: true, loadingText: '方案已选择！' });
      setTimeout(() => {
        this.addMessage('assistant', '好的，方案已选择！祝你周末愉快 🎉');
        this.setData({ loading: false });
      }, 500);
    } else if (action === 'reject') {
      this.addMessage('user', '都不喜欢，换一批');
      this.setData({ loading: true, loadingText: '正在重新生成方案...' });
      this.onSendMessage('都不喜欢，换一批');
    }
  },

  async onSendMessage(message) {
    try {
      const res = await api.sendChatMessage(message);
      this._handleResponse(res);
    } catch (err) {
      this.addMessage('assistant', '网络出了点问题，请稍后重试 😅');
    }
    this.setData({ loading: false });
  },
});
