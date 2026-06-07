"""
知识点数据库生成工具
======================
将 Day1~DayN 的知识点问答写入 SQLite 数据库，方便本地查询复习。

用法：
  python create_knowledge_db.py

输出：
  knowledge.db — SQLite 数据库文件（在脚本同级目录下）

查询示例：
  sqlite3 knowledge.db "SELECT * FROM qa WHERE day=1"
  sqlite3 knowledge.db "SELECT * FROM qa WHERE category='函数进阶'"
  sqlite3 knowledge.db "SELECT question FROM qa WHERE question LIKE '%args%'"
"""

import sqlite3
import os

# ── 数据库文件路径（和脚本在同一目录） ──
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge.db")

# ── 所有知识点数据 ──
# 每条数据格式：(day, category, question, answer)
QUESTIONS = [
    # ======================== Day 1 ========================

    # ── Conda 环境 ──
    (1, "Conda环境", "为什么 AI 开发需要虚拟环境？Conda 和 pip 的区别是什么？",
     """虚拟环境的必要性：不同 AI 项目依赖的 PyTorch/CUDA 版本可能冲突。

Conda vs pip：
- Conda：管理 Python + 系统库（如 CUDA），原生支持环境隔离
- pip：仅管理 Python 包，需要 venv/poetry 配合才能隔离

最佳实践：用 Conda 管理环境 + Python 版本，用 pip 装包。"""),

    (1, "Conda环境", "怎么创建一个叫 llm 的 Conda 环境？怎么激活和删除？",
     """创建：conda create -n llm python=3.11 -y
激活：conda activate llm
退出：conda deactivate
查看所有环境：conda env list
删除：conda remove -n llm --all

Trae 中选择：Ctrl+Shift+P → "Python: Select Interpreter" → 选 llm"""),

    (1, "Conda环境", ".env 文件是干什么的？为什么不能上传到 GitHub？",
     """.env 文件存敏感配置（API Key、数据库密码等）。
Python 通过 python-dotenv 加载：load_dotenv() → os.getenv("KEY")

不能上传的原因：API Key 泄露会导致别人盗用你的额度，造成经济损失。
正确做法：.env 加入 .gitignore，创建 .env.example 作为模板上传。"""),

    # ── Python 语法 ──
    (1, "Python语法", "Python 和 Swift 声明变量有什么核心区别？",
     """Python 不需要 let/var，直接 x = 1。
Python 没有真正的常量（全靠命名约定：全大写=常量）。
Python 变量是"动态类型"——同一个变量可以指向不同类型。
类型标注可选：x: int = 1（不写也行）。"""),

    (1, "Python语法", "Python 的缩进规则是什么？为什么缩进错了程序会崩溃？",
     """Python 用缩进代替大括号 {} 表示代码块。
缩进是语法的一部分，不对 = IndentationError。
规则：同一代码块缩进一致（标准 4 空格），不要混用 Tab 和空格。"""),

    (1, "Python语法", "Python 的列表（list）和字典（dict）怎么用？",
     """列表 list（≈ Swift Array）：[1,2,3]，支持 append、索引、切片。
列表推导式：[x**2 for x in range(10) if x%2==0]

字典 dict（≈ Swift Dictionary）：{"key": value}
遍历：for k, v in dict.items():
安全访问：dict.get("key", default)"""),

    (1, "Python语法", "range() 是什么？怎么用它写 for 循环？",
     """range() 生成整数序列。
range(5) → [0,1,2,3,4]
range(2,6) → [2,3,4,5]
range(0,10,2) → [0,2,4,6,8]

Swift 对照：
for i in 0..<5  → for i in range(5)
for i in 0...5  → for i in range(6)"""),

    (1, "Python语法", "Python 的字符串插值（f-string）怎么用？",
     """f-string：f"我叫{name}，今年{age}岁"
可以写表达式：f"明年我{age+1}岁"
格式化：f"成绩:{score:.2f}"，f"占比:{rate:.0%}"

Swift 对照：Python 用 f"…{var}…"，Swift 用 "…\\(var)…"。"""),

    (1, "Python语法", "Python 的 None 和 Swift 的 nil 有什么区别？",
     """Python 没有 Optional 类型，任何变量都可以是 None。
不需要解包，直接访问不会崩溃。
判断用 is not None，不是 == None。

Swift：String? 和 String 是不同类型，必须解包才能用。"""),

    (1, "Python语法", "列表推导式（List Comprehension）怎么写？",
     """语法：[表达式 for 变量 in 可迭代对象 if 条件]
示例：[x**2 for x in range(1, 11) if x % 2 == 0]
字典推导式：{k: v for k, v in dict.items() if 条件}

实际案例：[(city, temp) for city, temp in cities.items() if temp > 20]"""),

    (1, "Python语法", "Python 的 sorted() 函数怎么用？key 参数和 Lambda 怎么配合？",
     """sorted([3,1,4,1,5]) → [1,1,3,4,5]
sorted(列表, reverse=True) → 降序
sorted(列表, key=lambda x: x[1]) → 按第二个元素排序

Lambda 说明：lambda x: x[1] 意思就是"取每个元素的索引1作为排序依据"。"""),

    (1, "Python语法", "Python 的 if __name__ == '__main__': 的作用是什么？",
     """区分文件是直接运行还是被导入。
直接运行 → __name__ == "__main__" → 执行 if 内代码
被导入 → __name__ == 文件名 → 不执行

好处：一个文件既可以当脚本（python xxx.py），也可以当库（from xxx import ...）。"""),

    (1, "Python语法", "Python 的 def 函数怎么定义？和 Swift 的 func 有什么不同？",
     """def 函数名(参数: 类型 = 默认值) -> 返回类型:

与 Swift 的区别：
- 关键字：def vs func
- 函数体：冒号+缩进 vs 大括号
- Python 没有参数标签（Swift 有内外标签）"""),

    # ── PyTorch / GPU ──
    (1, "PyTorch/GPU", "怎么验证 PyTorch 能识别你的 RTX 5080？",
     """import torch
torch.cuda.is_available()  # → True
torch.cuda.get_device_name(0)  # → NVIDIA GeForce RTX 5080

先 nvidia-smi 确认驱动，再安装 CUDA 版 PyTorch。"""),

    (1, "PyTorch/GPU", "安装 PyTorch 时，CUDA 版本怎么选？",
     """CUDA 版本必须 ≤ 你显卡驱动的 CUDA 版本（nvidia-smi 查看）。
PyTorch 官方提供 cu118（11.8）、cu124（12.4）等版本。
RTX 5080 建议装 cu124：pip install torch ... --index-url https://download.pytorch.org/whl/cu124

装错版本 → torch.cuda.is_available() = False。"""),

    (1, "PyTorch/GPU", "RTX 5080 16GB 能用来做什么？多大参数的模型能跑？",
     """推理（4-bit量化）：7B✅ 14B✅ 32B✅（边界）
QLoRA 微调：7B✅ 14B✅ 32B❌
全参微调：全部❌（需要 H100 80GB）

总结：5080 16GB 足够覆盖 90% 的个人学习/研究实验。"""),

    # ── API 调用 ──
    (1, "API调用", "第一次调大模型 API 需要哪几步？最基本的代码怎么写？",
     """1. pip install openai python-dotenv
2. 创建 .env（写 API_KEY / API_BASE / MODEL）
3. 写代码：
   client = OpenAI(api_key=..., base_url=...)
   response = client.chat.completions.create(model=..., messages=[...])
   print(response.choices[0].message.content)

关键：messages 列表含 role（system/user/assistant）和 content。"""),

    (1, "API调用", "同步调用和流式调用有什么区别？什么时候该用哪种？",
     """同步（stream=False）：等全部生成完一次性返回 → 后台任务用
流式（stream=True）：逐字返回（打字机效果） → 聊天 UI 用

流式示例：for chunk in stream: print(chunk.choices[0].delta.content, end="")
需要自己拼接完整回复。"""),

    (1, "API调用", "System Prompt（系统提示词）有什么用？改它为什么 AI 性格会变？",
     """System Prompt 给 AI 设定角色/规则。
改它相当于给演员换剧本——AI 会按新角色的方式回复。
好的 system prompt 包含：角色 + 任务 + 输出格式 + 限制条件。"""),

    (1, "API调用", "OpenAI SDK 和 LM Studio / Ollama 有什么关系？",
     """OpenAI 的 API 格式成了行业标准，LM Studio、Ollama 等本地推理框架都兼容。
只要换 base_url，同一段代码可以调用不同服务：
- 官方：base_url="https://api.openai.com/v1"
- LM Studio：base_url="http://localhost:1234/v1"
- Ollama：base_url="http://localhost:11434/v1"  """),

    # ── 工具 / Git ──
    (1, "工具/Git", ".gitignore 是什么？Day1 项目应该忽略哪些文件？",
     """.gitignore 告诉 Git 不要跟踪某些文件。
Day1 必忽略：.env（API Key！）、__pycache__/、*.pyc、.venv/、.vscode/

如果不加 .gitignore 就 git add .，API Key 会泄露到 GitHub。"""),

    (1, "工具/Git", "第一天怎么用 Git 把代码推到 GitHub？",
     """git init → git branch -M main
先写 .gitignore
git add . → git commit -m "Day 1: ..."
git remote add origin https://... → git push -u origin main

后续：git add . → git commit -m "..." → git push"""),

    (1, "工具/Git", "Trae IDE 有哪些必装插件？怎么选择 Python 解释器？",
     """必装：Python 官方、Pylance（类型检查）、Jupyter、GitLens、Black Formatter、Ruff
选择解释器：Ctrl+Shift+P → "Python: Select Interpreter" → 选 llm
成功标志：右下角显示 "Python 3.11.x ('llm')"""),


    # ======================== Day 2 ========================

    # ── 函数进阶 ──
    (2, "函数进阶", "位置参数和关键字参数有什么区别？单独的 * 怎么用？",
     """位置参数：按传入顺序匹配参数名。
关键字参数：用 name=value 指定参数名，顺序可任意。
单独的 * 表示后面的参数只能用关键字传参（强制明确）。

def f(a, b, *, c, d):  # c 和 d 必须用关键字传参
    pass"""),

    (2, "函数进阶", "*args 是什么？怎么用？",
     """*args 接收任意数量的位置参数，内部是一个 tuple。
def sum_all(*args): return sum(args)
拆包调用：sum_all(*[1,2,3]) 等价于 sum_all(1,2,3)

类比 Swift 可变参数：func sum(_ numbers: Int...)"""),

    (2, "函数进阶", "**kwargs 是什么？和 *args 有什么区别？",
     """**kwargs 接收任意数量的关键字参数，内部是一个 dict。
*args → tuple，**kwargs → dict
拆包调用：func(**{"key": "val"}) 等价于 func(key="val")

AI 库大量使用 **kwargs 透传参数给底层。"""),

    (2, "函数进阶", "默认参数陷阱是什么？def f(x=[]) 为什么是坑？",
     """默认参数只在函数定义时创建一次，所有调用共享同一个对象。

def add(item, items=[]):  # 坑！
    items.append(item)
    return items
add("a") → ['a']; add("b") → ['a','b']  # 不是 ['b']！

正确写法：def add(item, items=None):
    if items is None: items = []"""),

    (2, "函数进阶", "Lambda 函数是什么？和 Swift 闭包有什么对应关系？",
     """Lambda = 匿名函数，一行写完，自动 return。
lambda x: x * 2  # 等价于 def double(x): return x*2
常用于排序 key、map、filter。

Swift 对照：{ $0 * 2 } vs lambda x: x*2
限制：Lambda 只能写一个表达式，不能写语句。"""),

    (2, "函数进阶", "闭包（Closure）是什么？怎么用 nonlocal？",
     """闭包：内部函数"记住"外部函数的变量，即使外部函数已执行完毕。
nonlocal 声明要修改外部函数的变量（不加的话会创建新的局部变量）。

实际应用：装饰器本质就是用闭包实现的。"""),

    (2, "函数进阶", "装饰器（Decorator）的原理是什么？和闭包的关系？",
     """装饰器 = 接收函数、返回新函数的函数（底层就是闭包）。
@timer 等价于 func = timer(func)
装饰器是闭包的典型应用——用闭包包装另一个函数，添加额外逻辑。

FastAPI、Flask、pytest 大量使用装饰器（@app.get、@pytest.fixture）。"""),

    # ── 面向对象 ──
    (2, "面向对象", "Python 的 class 和 Swift 的 class 核心区别是什么？",
     """- self 必须显式写（Swift 隐式）
- 构造函数叫 __init__（Swift 叫 init）
- 没有 access control（用 _ 约定私有）
- Python 属性直接在 __init__ 里 self.x = x
- @property ≈ Swift computed property
- 打印对象用 __str__/__repr__ ≈ CustomStringConvertible"""),

    (2, "面向对象", "self 在 Python 里为什么必须写？",
     """Python 设计哲学：显式优于隐式（Explicit is better than implicit）。
方法本质是函数，instance.method() 等价于 Class.method(instance)。
所以必须用 self 明确接收实例本身。"""),

    (2, "面向对象", "@property 是什么？等于 Swift 的什么？",
     """@property 把方法变成像属性一样访问（不加括号）。
等于 Swift 的计算属性（computed property）。
也可以设置 setter：@属性名.setter

LLMClient 中 history_length 就是用 @property 实现的。"""),

    (2, "面向对象", "@dataclass 是什么？它自动帮我们生成了什么？",
     """@dataclass 自动生成：__init__、__repr__、__eq__。
相当于省去大量重复代码。
≈ Swift 的 struct（自动生成初始化器和 Equatable 等）。"""),

    (2, "面向对象", "field(default_factory=...) 是什么？为什么需要它？",
     """解决 dataclass 中可变默认值的共享问题。
@dataclass 也不允许直接用可变对象做默认值（同"默认参数陷阱"）。
field(default_factory=list) → 每次创建实例时都新建一个空列表。

常用于：从环境变量读配置、创建空列表/字典。"""),

    (2, "面向对象", "__post_init__ 是什么？什么时候会被调用？",
     """dataclass 的钩子方法，在 __init__ 执行完后自动调用。
用途：做额外初始化（创建其他对象、调用方法）。
LLMClient 中用 __post_init__ 创建 OpenAI 客户端和初始化历史列表。"""),

    (2, "面向对象", "Python 的 _private 约定和 Swift 的 private 有什么区别？",
     """Python 没有真正的 private！全靠下划线约定：
- _single：约定"我私有的，你不要动"
- __double：触发 name mangling（变成 _ClassName__attr）

Python 哲学：We are all consenting adults（我们是成年人，靠自觉）。"""),

    (2, "面向对象", "__str__ 和 __repr__ 是什么？有什么区别？",
     """__repr__：给开发者看，应包含足够信息（调试用）
__str__：给用户看，要简洁美观
print(obj) 调用 __str__，repr(obj) 调用 __repr__
如果没有 __str__，会退回到 __repr__

≈ Swift 的 CustomDebugStringConvertible 和 CustomStringConvertible。"""),

    (2, "面向对象", "Python 如何实现继承？子类怎么调用父类方法？",
     """class Dog(Animal):  # 括号里写父类
子类重写方法同名即可。
调用父类：super().__init__(name) / super().speak()

和 Swift 一样，Python 用 super()，Swift 用 super。"""),

    # ── LLMClient ──
    (2, "LLMClient", "LLMClient 的 chat() 和 stream_chat() 有什么区别？",
     """chat()：同步，等全部生成完一次性返回字符串 → 后台任务
stream_chat()：流式，逐字返回（yield）→ 聊天 UI（打字机效果）

API 参数：stream=False（默认）vs stream=True"""),

    (2, "LLMClient", "LLMClient 的 _history 是干什么的？对话历史怎么维护？",
     """_history 是 List[ChatMessage]，按顺序存所有消息。
大模型本身没有记忆，每次调用 API 都要把全部历史传过去。
初始化：system 消息 → 用户说 → 加 user 消息 → AI 回复 → 加 assistant 消息

reset() 清空历史只保留 system prompt，相当于"开启新对话"。"""),

    (2, "LLMClient", "reset() 和 set_system() 的区别是什么？",
     """reset()：清空历史 + 用当前 system_prompt 重建 → 重新聊（人设不变）
set_system(prompt)：换 system_prompt + 调 reset() → 换人设

set_system 内部就是调用了 reset()。"""),

    (2, "LLMClient", "CLI 中的 if __name__ == '__main__': 是什么？",
     """只有直接运行这个文件时才执行 main()，被 import 时不执行。
使文件既可以当脚本（python cli.py），也可以当模块（from cli import main）。"""),

    (2, "LLMClient", "生成器（Generator）和 yield 是怎么工作的？",
     """生成器可以"暂停和恢复"。yield 暂停函数，返回一个值，下次调用从暂停处继续。
stream_chat 中：API 返回 chunk → yield delta（每收到一个字就返回给调用方）
和 return 的区别：return 结束函数，yield 暂停函数。"""),

    # ── pytest ──
    (2, "pytest", "pytest 的基本规则是什么？怎么命名测试函数？",
     """文件名以 test_ 开头或 _test 结尾。
函数名以 test_ 开头。
命名不对 → pytest 直接忽略，不会报错。

运行：pytest 文件名.py -v（-v 详细输出）"""),

    (2, "pytest", "assert 在测试中怎么用？和普通 Python assert 有区别吗？",
     """没有区别，就是同一个 assert 关键字。
assert 条件 → True 通过，False 抛出 AssertionError。
pytest 增强了错误信息显示（会展示实际值和期望值以及表达式路径）。"""),

    (2, "pytest", "Mock 是什么？为什么测试 LLMClient 需要它？",
     """Mock = "假对象"，代替真实对象，控制其行为。
测试 chat() 如果不 mock → 真的去调 API（需要网络、花钱、依赖外部服务）。
用 Mock 后：速度快、稳定、不依赖外部、可以模拟各种极端情况。"""),

    (2, "pytest", "mocker.patch.object() 是做什么的？",
     """把真实对象的某个方法临时替换成假的。
mocker.patch.object(obj, "method", return_value=fake_value)
替换只在当前测试函数内生效，测试结束后自动恢复。"""),

    (2, "pytest", "Mock 如何模拟 API 响应？response.choices[0].message.content 这个结构怎么来的？",
     """来自 OpenAI API 的响应格式（嵌套字典）。
Mock 对象访问任何属性都不会报错，自动创建子 Mock。
mock_response.choices = [mocker.Mock()]
mock_response.choices[0].message.content = "mocked reply"

这样 mock_response 的结构就和真实 API 响应一致了。"""),
]


def create_database():
    """创建 SQLite 数据库并插入所有知识点数据。"""
    # 删除旧数据库
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            day         INTEGER NOT NULL,           -- 第几天
            category    TEXT    NOT NULL,            -- 分类
            question    TEXT    NOT NULL UNIQUE,      -- 问题
            answer      TEXT    NOT NULL,             -- 解答
            created_at  TEXT    DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # 插入数据
    cursor.executemany(
        "INSERT OR IGNORE INTO qa (day, category, question, answer) VALUES (?, ?, ?, ?)",
        QUESTIONS
    )

    conn.commit()

    # 统计
    count = cursor.execute("SELECT COUNT(*) FROM qa").fetchone()[0]
    days = cursor.execute("SELECT DISTINCT day FROM qa ORDER BY day").fetchall()
    categories = cursor.execute("SELECT DISTINCT category FROM qa ORDER BY category").fetchall()

    conn.close()

    print(f"✅ 数据库创建成功: {DB_PATH}")
    print(f"   共 {count} 条知识点")
    print(f"   涵盖天数: {', '.join(str(d[0]) for d in days)}")
    print(f"   分类: {', '.join(c[0] for c in categories)}")
    print()
    print("📖 查询示例：")
    print("  使用 sqlite3 命令行：")
    print(f'  sqlite3 "{DB_PATH}"')
    print("  sqlite> .headers on")
    print("  sqlite> SELECT day, category, question FROM qa WHERE day=1 LIMIT 5;")
    print()
    print("  使用 Python：")
    print("  import sqlite3")
    print(f'  conn = sqlite3.connect("{DB_PATH}")')
    print('  cursor = conn.cursor()')
    print('  for row in cursor.execute("SELECT question FROM qa WHERE category LIKE \\"%函数%\\""):')
    print('      print(row[0])')


if __name__ == "__main__":
    create_database()