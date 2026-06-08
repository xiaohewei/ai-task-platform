# Godot 学习报告

**日期**：2026年6月7日  
**学习时长**：约4小时  
**学习范围**：基本操作 → 脚本编程

---

## 一、学习概览

今天的学习从零开始接触 Godot 引擎，完成了从界面认知到编写第一段 GDScript 脚本的完整入门流程。学习方式以动手实践为主，边学边练。

---

## 二、学习内容

### 1. Godot 基本操作（约1.5小时）

#### 1.1 界面认知
- **场景面板（Scene）**：以树形结构展示当前场景中所有节点，是管理节点层级关系的核心视图。
- **文件系统（FileSystem）**：项目资源管理器，支持拖拽导入纹理、音频、脚本等资源。
- **检视器（Inspector）**：选中节点后显示其属性面板，可修改节点的位置、旋转、缩放及其他组件属性。
- **视口（Viewport）**：编辑场景的 2D/3D 视图窗口，支持多视图切换。
- **输出/调试器（Output/Debugger）**：查看运行日志和调试信息。

#### 1.2 视口导航
| 操作 | 快捷键/方式 |
|------|------------|
| 平移视图 | 鼠标中键拖拽 |
| 缩放视图 | 鼠标滚轮 |
| 聚焦选中节点 | F 键 |
| 切换 2D/3D/脚本视图 | 顶部工具栏切换 |
| 运行项目 | F5 |
| 运行当前场景 | F6 |

#### 1.3 项目创建
- 通过项目管理器创建新项目，选择渲染器（Forward+ / Mobile / Compatibility）。
- 理解项目目录结构：`scenes/`、`scripts/`、`assets/` 等组织方式。
- 配置项目设置：窗口尺寸、输入映射（Input Map）等。

### 2. 节点与场景系统（约1小时）

#### 2.1 节点（Node）概念
- Godot 的核心设计理念：**一切皆节点**。
- 常用节点类型：
  - `Node2D` — 2D 游戏对象的基类
  - `Sprite2D` — 显示 2D 纹理
  - `CollisionShape2D` — 碰撞形状
  - `Area2D` — 检测区域
  - `CharacterBody2D` — 物理角色控制器
  - `Label` / `Button` — UI 控件
  - `Timer` — 计时器节点

#### 2.2 场景（Scene）系统
- 场景是节点的集合，以 `.tscn` 文件保存。
- **场景实例化**：一个场景可以作为子节点添加到另一个场景中，实现模块化。
- 场景的层级关系与继承：子节点随父节点一起变换（移动、旋转、缩放）。
- 实践：创建玩家场景、敌人场景，并在主场景中实例化。

#### 2.3 信号（Signal）机制
- 信号是 Godot 内置的观察者模式实现。
- 常用信号：`body_entered`、`pressed`、`timeout`、`ready`。
- 信号连接方式：编辑器可视化连接 + 代码连接两种方式。

### 3. GDScript 脚本入门（约1.5小时）

#### 3.1 GDScript 基础语法
```gdscript
# 变量声明与类型
var speed: float = 400.0
var health: int = 100
var player_name: String = "Player"
var is_alive: bool = true

# 常量
const GRAVITY: float = 980.0
const MAX_SPEED: int = 600

# 数组与字典
var items: Array = ["sword", "shield"]
var player_data: Dictionary = {
    "name": "Hero",
    "level": 1
}
```

#### 3.2 核心生命周期函数
```gdscript
extends Node2D

# 节点进入场景树时调用（初始化）
func _ready():
    print("节点已就绪")

# 每帧调用一次
func _process(delta: float):
    # delta 是上一帧的时间间隔（秒），用于帧率无关的运动
    position.x += speed * delta

# 每物理帧调用（固定 60Hz）
func _physics_process(delta: float):
    # 物理相关逻辑放这里
    pass
```

#### 3.3 输入处理
```gdscript
func _process(delta: float):
    var direction: Vector2 = Vector2.ZERO
    
    if Input.is_action_pressed("ui_right"):
        direction.x += 1
    if Input.is_action_pressed("ui_left"):
        direction.x -= 1
    if Input.is_action_pressed("ui_down"):
        direction.y += 1
    if Input.is_action_pressed("ui_up"):
        direction.y -= 1
    
    position += direction.normalized() * speed * delta
```

#### 3.4 信号连接（代码方式）
```gdscript
func _ready():
    $Button.pressed.connect(_on_button_pressed)
    $Area2D.body_entered.connect(_on_body_entered)

func _on_button_pressed():
    print("按钮被按下")

func _on_body_entered(body: Node2D):
    print("物体进入区域:", body.name)
```

#### 3.5 获取节点引用
```gdscript
# $ 语法糖，等价于 get_node()
@onready var sprite: Sprite2D = $Sprite2D
@onready var animation_player: AnimationPlayer = $AnimationPlayer

# @onready 确保在 _ready() 调用前初始化
```

#### 3.6 实践项目：简易移动角色
今天完成了一个简易的 2D 角色移动 Demo，实现了：
- 键盘 WASD 控制角色八方向移动
- 使用 `CharacterBody2D` + `move_and_slide()` 处理碰撞
- 速度归一化防止斜向移动过快
- 基础的动画切换（idle / walk）

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _physics_process(delta: float):
    var direction: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = direction * speed
    move_and_slide()
    
    if direction.length() > 0:
        anim.play("walk")
    else:
        anim.play("idle")
```

---

## 三、学习收获与心得

| 收获 | 说明 |
|------|------|
| 理解了 Godot 的节点架构 | 以节点树为核心的场景组织方式，与 Unity 的 GameObject-Component 模式有所不同，更加轻量和直观 |
| 掌握了场景与实例化 | 场景嵌套与继承是 Godot 模块化开发的基础 |
| 信号机制 | 松耦合的通信方式，比直接调用更灵活 |
| GDScript 上手 | 语法类 Python，学习曲线平缓，`$` 语法糖非常方便 |
| `_process` vs `_physics_process` | 理解了渲染帧与物理帧的区别，以及对运动逻辑的影响 |

---

## 四、后续学习计划

1. **动画系统深入**：AnimationPlayer 的关键帧动画与混合树（AnimationTree）。
2. **TileMap**：制作瓦片地图，搭建关卡。
3. **UI 系统**：血量条、分数显示、菜单界面。
4. **音效与音乐**：AudioStreamPlayer 的使用。
5. **导出与发布**：了解 Godot 的跨平台导出流程。
6. **Shader 入门**：Godot 的着色器语言。

---

## 五、遇到的问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 角色移动时斜向速度过快 | 未对方向向量归一化 | 使用 `direction.normalized()` |
| 脚本中节点引用为 null | 节点路径错误或使用了 `get_node()` 但节点还未就绪 | 使用 `@onready` 或 `$` 语法糖，并检查节点路径 |
| `move_and_slide()` 不生效 | 节点类型用了 `Node2D` 而非 `CharacterBody2D` | 将根节点改为 `CharacterBody2D` |

---

## 六、总结

今天4小时的 Godot 学习从零基础起步，覆盖了引擎基本操作、节点系统、场景管理以及 GDScript 脚本编程。通过动手实践完成了一个简易 2D 角色移动 Demo，对 Godot 的开发流程有了整体认知。下一步计划深入动画系统和 TileMap 关卡编辑。

> "The best way to learn is by doing." —— 今天的学习再次印证了这一点。

---

*报告由 Claude Code 辅助生成*
