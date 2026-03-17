"""Plan service: plan generation orchestrator (W1 mock)."""

import uuid

from app.models.schemas import PlanCard, PlanDetail, PlanSource, PlanStop, UserContext


# Pre-generated mock plan IDs for consistent detail lookups
MOCK_PLAN_A_ID = "mock-plan-a-001"
MOCK_PLAN_B_ID = "mock-plan-b-001"


class PlanService:
    """Generates weekend plans. W1: returns hardcoded mock data."""

    def generate_mock_plans(self, ctx: UserContext) -> list[PlanCard]:
        """Return 2 sample plans based on the 双塔市集 example from PRD."""
        city = ctx.city or "苏州"
        tags = ["免费", "有餐饮"]
        if "孕妇" in ctx.constraints:
            tags.insert(0, "孕妇友好")
        if "人少" in ctx.preferences:
            tags.insert(0, "人少")

        plan_a = PlanCard(
            plan_id=MOCK_PLAN_A_ID,
            title="双塔市集赏花散步",
            emoji="🌸",
            description="玉兰花季，吃喝逛一条线",
            duration="半天（3-4小时）",
            cost_range="50元以内",
            transport="地铁+步行",
            tags=tags,
            stops_count=4,
            source_count=3,
        )

        plan_b = PlanCard(
            plan_id=MOCK_PLAN_B_ID,
            title=f"{city}博物馆文艺之旅",
            emoji="🏛️",
            description="看展逛馆，咖啡收尾",
            duration="半天（3-4小时）",
            cost_range="30元以内",
            transport="地铁+步行",
            tags=["室内为主", "文艺", "免费"] + (["孕妇友好"] if "孕妇" in ctx.constraints else []),
            stops_count=3,
            source_count=2,
        )

        return [plan_a, plan_b]

    def get_mock_detail(self, plan_id: str) -> PlanDetail:
        """Return mock plan detail."""
        if plan_id == MOCK_PLAN_A_ID:
            return PlanDetail(
                plan_id=plan_id,
                title="双塔市集赏花散步",
                stops=[
                    PlanStop(
                        name="双塔市集",
                        arrive_at="10:00",
                        stay_duration="30-45分钟",
                        recommendation="老客满蛋饼 + 冰豆浆",
                        nav_link="https://uri.amap.com/marker?position=120.636,31.316&name=双塔市集",
                        walk_to_next="240m, 约3分钟",
                    ),
                    PlanStop(
                        name="定慧寺巷",
                        arrive_at="10:45",
                        stay_duration="20分钟",
                        recommendation="玉兰花拍照打卡",
                        nav_link="",
                        walk_to_next="500m, 约6分钟",
                    ),
                    PlanStop(
                        name="耦园",
                        arrive_at="11:15",
                        stay_duration="45-60分钟",
                        recommendation="世界文化遗产，人少清净",
                        nav_link="https://uri.amap.com/marker?position=120.643,31.318&name=耦园",
                        walk_to_next="300m, 约4分钟",
                    ),
                    PlanStop(
                        name="相门城墙",
                        arrive_at="12:15",
                        stay_duration="30分钟",
                        recommendation="城墙上散步看护城河",
                        nav_link="",
                        walk_to_next="",
                    ),
                ],
                tips=[
                    "明天 7-15°C 多云，建议穿薄外套",
                    "全程步行约 1.6km，平路为主，孕妇友好",
                    "双塔市集周一休市，请注意时间",
                ],
                sources=[
                    PlanSource(title="苏州赏花路线合集", likes=2340, url="https://example.com/1"),
                    PlanSource(title="双塔市集必吃攻略", likes=1820, url="https://example.com/2"),
                    PlanSource(title="苏州半日游路线", likes=956, url="https://example.com/3"),
                ],
            )

        # Default fallback for plan B or unknown
        return PlanDetail(
            plan_id=plan_id,
            title="博物馆文艺之旅",
            stops=[
                PlanStop(
                    name="苏州博物馆",
                    arrive_at="09:30",
                    stay_duration="1.5-2小时",
                    recommendation="贝聿铭设计，免费预约",
                    nav_link="https://uri.amap.com/marker?position=120.628,31.322&name=苏州博物馆",
                    walk_to_next="800m, 约10分钟",
                ),
                PlanStop(
                    name="平江路",
                    arrive_at="11:30",
                    stay_duration="1小时",
                    recommendation="逛小店 + 午餐",
                    nav_link="",
                    walk_to_next="200m, 约2分钟",
                ),
                PlanStop(
                    name="猫的天空之城",
                    arrive_at="12:30",
                    stay_duration="30-45分钟",
                    recommendation="写明信片 + 咖啡",
                    nav_link="",
                    walk_to_next="",
                ),
            ],
            tips=[
                "苏州博物馆需提前预约，免费",
                "平江路人流较大，建议避开下午高峰",
            ],
            sources=[
                PlanSource(title="苏州博物馆攻略", likes=3100, url="https://example.com/4"),
                PlanSource(title="平江路美食地图", likes=1560, url="https://example.com/5"),
            ],
        )
