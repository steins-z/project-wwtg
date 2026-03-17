// components/plan-card/plan-card.js — 方案卡片组件
Component({
  properties: {
    plan: {
      type: Object,
      value: {},
    },
  },

  methods: {
    onTap() {
      this.triggerEvent('tap', { planId: this.data.plan.plan_id });
    },
  },
});
