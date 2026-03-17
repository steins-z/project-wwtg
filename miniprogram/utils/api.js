// utils/api.js — API 客户端
const app = getApp();

/**
 * 通用请求封装
 */
function request(path, options = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.baseURL + path,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...options.header,
      },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res);
        }
      },
      fail(err) {
        reject(err);
      },
    });
  });
}

/**
 * 发送聊天消息
 * W1 note: SSE not supported in wx.request — falls back to regular POST with mock response
 */
async function sendChatMessage(message) {
  if (app.globalData.mockMode) {
    // Mock response for W1 development
    return {
      reply: '为您找到以下方案：',
      plans: [
        {
          plan_id: 'mock-plan-a-001',
          title: '双塔市集赏花散步',
          emoji: '🌸',
          description: '玉兰花季，吃喝逛一条线',
          duration: '半天（3-4小时）',
          cost_range: '50元以内',
          transport: '地铁+步行',
          tags: ['孕妇友好', '人少', '免费', '有餐饮'],
          stops_count: 4,
          source_count: 3,
        },
        {
          plan_id: 'mock-plan-b-001',
          title: '博物馆文艺之旅',
          emoji: '🏛️',
          description: '看展逛馆，咖啡收尾',
          duration: '半天（3-4小时）',
          cost_range: '30元以内',
          transport: '地铁+步行',
          tags: ['室内为主', '文艺', '免费'],
          stops_count: 3,
          source_count: 2,
        },
      ],
    };
  }

  return request('/chat/message', {
    method: 'POST',
    data: { message, session_id: app.globalData.sessionId },
  });
}

/**
 * 获取方案详情
 */
async function getPlanDetail(planId) {
  if (app.globalData.mockMode) {
    return {
      plan_id: planId,
      title: '双塔市集赏花散步',
      stops: [
        { name: '双塔市集', arrive_at: '10:00', stay_duration: '30-45分钟', recommendation: '老客满蛋饼 + 冰豆浆', walk_to_next: '240m, 约3分钟' },
        { name: '定慧寺巷', arrive_at: '10:45', stay_duration: '20分钟', recommendation: '玉兰花拍照打卡', walk_to_next: '500m, 约6分钟' },
        { name: '耦园', arrive_at: '11:15', stay_duration: '45-60分钟', recommendation: '世界文化遗产，人少清净', walk_to_next: '300m, 约4分钟' },
        { name: '相门城墙', arrive_at: '12:15', stay_duration: '30分钟', recommendation: '城墙上散步看护城河', walk_to_next: '' },
      ],
      tips: ['明天 7-15°C 多云，建议穿薄外套', '全程步行约 1.6km，平路为主'],
      sources: [
        { title: '苏州赏花路线合集', likes: 2340 },
        { title: '双塔市集必吃攻略', likes: 1820 },
      ],
    };
  }

  return request('/plan/detail/' + planId);
}

module.exports = { request, sendChatMessage, getPlanDetail };
