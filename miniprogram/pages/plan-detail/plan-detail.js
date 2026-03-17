// pages/plan-detail/plan-detail.js — 方案详情页
const api = require('../../utils/api');

Page({
  data: {
    plan: null,
    loading: true,
  },

  onLoad(options) {
    const planId = options.id;
    if (planId) {
      this.loadPlanDetail(planId);
    }
  },

  async loadPlanDetail(planId) {
    try {
      const plan = await api.getPlanDetail(planId);
      this.setData({ plan, loading: false });
    } catch (err) {
      console.error('Failed to load plan:', err);
      this.setData({ loading: false });
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  // 打开导航
  onNavigate(e) {
    const { name, lat, lng } = e.currentTarget.dataset;
    if (lat && lng) {
      wx.openLocation({
        latitude: parseFloat(lat),
        longitude: parseFloat(lng),
        name: name,
        scale: 16,
      });
    }
  },
});
