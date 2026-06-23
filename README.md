# 学习营地

> 广东工业大学 大二下 · 暑期实习备战 · AI Coding 全栈方向
>
> 完整代码 + 踩坑笔记

---

## 作品展示

### [AI 辅助任务管理平台](task-manager/)

> FastAPI + SQLAlchemy + JWT + 原生 JS 前端

- 用户注册 / 登录（JWT + bcrypt 加密）
- 任务 CRUD（创建、编辑、删除）
- 优先级标记（高/中/低）+ 状态流转（待办→进行中→已完成）
- 筛选过滤 + RESTful API + SQLite 持久化

```bash
cd task-manager/
pip install fastapi uvicorn sqlalchemy passlib python-jose
uvicorn main:app --reload
# 打开 http://127.0.0.1:8000
```

---

## 学习路线（40 天全计划）

### 第 1 周：Python 全栈基础

| 天 | 内容 | 文件 |
|:--:|------|------|
| Day1 | Hello World + SQLite CRUD | `days/day1-hello/` |
| Day2 | 路径参数 / 查询参数 / Pydantic + POST | `days/day2-params/` |
| Day3 | FastAPI + SQLite 完整 CRUD API | `days/day3-crud/` |
| Day4 | SQLAlchemy ORM | `days/day4-orm/` |
| Day5 | FastAPI + ORM 集成 | `days/day5-fastapi-orm/` |
| Day5-alt | 数据库迁移 + 标准项目结构 | `days/day5-migration/` |
| Day6 | JWT 用户认证 | `days/day6-auth/` |
| Day7 | 静态文件 / 文件下载 / 子应用 | `days/day7-static-mount/` |

### 第 2 周：前端基础 + AI 工具链

| 天 | 内容 | 文件 |
|:--:|------|------|
| Day8 | HTML 基础（标签/表单/语义化） | `days/day8-html-basics/` |
| Day9 | CSS 基础（选择器/盒模型/Flex） | `days/day9-css-basics/` |
| Day10 | CSS 进阶（Grid/响应式/动画） | `days/day10-css-advanced/` |
| Day11 | JavaScript 基础（变量/函数/DOM） | `days/day11-js-basics/` |
| Day12 | JS 异步（Promise/fetch/async） | `days/day12-js-async/` |
| Day13 | AI 工具链：Cursor / Copilot | `days/day13-ai-toolchain/` |
| Day14 | Prompt Engineering 实战 | `days/day14-prompt-engineering/` |

### 第 3 周：全栈项目攻坚

| 天 | 内容 | 文件 |
|:--:|------|------|
| Day15 | Vue3 基础（响应式/模板/指令） | `days/day15-vue3-basics/` |
| Day16 | Vue3 组件化（Props/Emits/插槽） | `days/day16-vue3-components/` |
| Day17 | 任务平台前端：登录注册页 | `days/day17-task-frontend-login/` |
| Day18 | 任务平台前端：任务 CRUD | `days/day18-task-frontend-crud/` |
| Day19 | 前后端联调（上）：axios 封装 | `days/day19-api-integration/` |
| Day20 | 前后端联调（下）：登录态与错误处理 | `days/day20-api-integration-2/` |
| Day21 | Docker 入门 + 容器化部署 | `days/day21-docker/` |

### 第 4 周：项目打磨 + 算法突击

| 天 | 内容 | 文件 |
|:--:|------|------|
| Day22 | 项目功能完善：搜索 + 筛选 | `days/day22-project-polish-1/` |
| Day23 | 项目功能完善：导出 + 分页优化 | `days/day23-project-polish-2/` |
| Day24 | 数据库优化：索引 + 查询分析 | `days/day24-db-optimize-1/` |
| Day25 | 数据库优化：N+1 + 连接池 | `days/day25-db-optimize-2/` |

---

## 技术栈总览

```
后端：  Python · FastAPI · SQLAlchemy · JWT · Pydantic · SQLite
前端：  HTML5 · CSS3 · JavaScript · Vue3
工具：  Git · GitHub · Docker · uvicorn · VS Code
```

---

*2026 暑期实习备战中 · 25 天系统学习*
