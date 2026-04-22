# shared-constants-dedup

## 问题

相同含义的常量值在多处独立定义时，修改一处容易遗漏另一处，导致校验逻辑和修复逻辑使用不同的值集合。

## 踩坑记录

步骤16中合法媒体比例列表在 `applyStyleFallback()` 和 `checkMediaRatioSafety()` 两处独立定义。如果需要新增合法比例（如 "21:9"），两处都要改，漏改一处会导致校验通过但修复时被替换为默认值。

## 规则

**发现两个及以上位置使用相同字面量数组/对象时，立即提取为 export const 共享常量。**

命名规范：`VALID_<DOMAIN>_<NAME>`（如 VALID_MEDIA_RATIOS、DEFAULT_BRAND_COLORS）

## 适用范围

所有模块中存在重复字面量数组和对象的场景。

## 来源

步骤16 Code Reviewer（2026-04-15），confidence: 0.9
