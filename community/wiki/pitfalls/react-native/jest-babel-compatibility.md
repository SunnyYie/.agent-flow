---
name: jest-babel-compatibility
type: pitfall
module: react-native
status: verified
confidence: 0.85
created: 2026-04-13
tags: [jest, babel, react-native, testing, mocha]
---

# 旧版 React Native 项目的 Jest 兼容性问题

> RN 0.6x 项目（Babel 7.12.x）无法运行新版 Jest 插件（需 ^7.22.0）

## 问题描述

React Native 0.69 项目使用 Babel 7.12.x，而新版 Jest 插件（如 @babel/plugin-syntax-import-attributes）需要 Babel ^7.22.0。运行 Jest 时会报版本不兼容错误，导致测试套件无法加载。

`agent-flow qa` 也可能检测到 Jest 并默认运行，但项目实际用 Mocha，导致 QA 阶段误报失败。

## 解决方案

1. 使用项目原有的 Mocha 测试框架（`npm test`）
2. Mocha 测试文件放在 `test/` 目录，使用 `@babel/register` + `@babel/polyfill`
3. 用 `npm test -- --grep "pattern"` 运行指定测试
4. 如必须用 Jest，需升级 Babel 或锁定插件版本
5. agent-flow qa 阶段应手动指定 Mocha 测试或跳过 Jest 门控

## 相关条目
