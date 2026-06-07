"""
测试文件：test_llm_client.py
==========================================
这个文件用来测试 llm_client.py 中的 LLMClient 和 ChatMessage 类。
我们用 pytest 框架来写测试，确保代码的正确性。

为什么要写测试？
  - 修改代码后，运行测试可以快速知道有没有破坏现有的功能
  - 测试本身就是"可执行的文档"，告诉别人这段代码应该怎么用
  - 在重构（重写代码但不改功能）时提供安全保障

如何运行测试？
  pytest test_llm_client.py -v
  # -v 表示 verbose（详细输出），会显示每个测试的名字和结果
"""

# 导入 pytest 测试框架
import pytest
# 从 llm_client.py 导入我们要测试的两个类
from llm_client import LLMClient, ChatMessage


# ══════════════════════════════════════════════════════════
# 测试 1：测试 ChatMessage 的 to_dict() 方法
# ══════════════════════════════════════════════════════════
def test_chat_message_to_dict():
    """
    测试目标：验证 ChatMessage 能否正确转换为字典格式。

    背景知识：
      - ChatMessage 是一个数据类（@dataclass），用来存一条消息
      - 每条消息有 role（角色：user/assistant/system）和 content（内容）
      - to_dict() 方法把消息转成 {"role": "...", "content": "..."} 的格式
      - API 调用时需要这种字典格式

    这个测试：
      1. 创建一个用户消息 "你好"
      2. 断言 to_dict() 的返回值是否等于预期的字典
    """
    message = ChatMessage(role="user", content="你好")
    assert message.to_dict() == {"role": "user", "content": "你好"}


# ══════════════════════════════════════════════════════════
# 测试 2：测试 LLMClient 初始化（创建实例时）的状态
# ══════════════════════════════════════════════════════════
def test_client_initialization():
    """
    测试目标：创建一个 LLMClient 实例后，检查默认值是否正确。

    背景知识：
      - LLMClient 类的 __post_init__ 方法会在创建实例时自动执行
      - 初始化时会调用 reset()，reset() 会把一条 system 消息加入历史
        所以 history_length 初始值是 1（那一条 system 消息）
      - temperature 默认是 0.7

    这个测试：
      1. 创建一个客户端
      2. 断言历史记录长度为 1（只有系统提示词）
      3. 断言温度参数为 0.7（默认值）
    """
    client = LLMClient()
    assert client.history_length == 1
    assert client.temperature == 0.7


# ══════════════════════════════════════════════════════════
# 测试 3：测试 reset() 方法能否清空对话历史
# ══════════════════════════════════════════════════════════
def test_reset_clears_history():
    """
    测试目标：验证 reset() 能清空历史，但保留系统提示词。

    背景知识：
      - _history 是一个列表，存着所有对话消息
      - history_length 是 @property，返回 len(self._history)
      - reset() 会清空列表，然后重新加入 system 消息
      - 注意：_history 是列表（list），不能直接和数字比较！
        要比较长度得用 history_length 属性，或者 len(client._history)

    这个测试：
      1. 创建一个客户端（此时 history_length == 1，有一条 system 消息）
      2. 手动追加一条用户消息（此时 history_length == 2）
      3. 调用 reset() 重置
      4. 断言历史长度恢复为 1（只有 system 消息）
    """
    client = LLMClient()
    # 手动往历史列表加一条用户消息，模拟对话过
    client._history.append(ChatMessage(role="user", content="test"))
    assert client.history_length == 2  # system + user = 2 条

    # 调用 reset()，应该清空历史再重新加 system 消息
    client.reset()
    assert client.history_length == 1  # 只剩 system 消息


# ══════════════════════════════════════════════════════════
# 测试 4：测试 set_system() 方法更换系统提示词
# ══════════════════════════════════════════════════════════
def test_set_system_resets():
    """
    测试目标：验证 set_system() 能更换系统提示词并重置对话。

    背景知识：
      - set_system(prompt) 做了两件事：
        1. 把 self.system_prompt 换成新的提示词
        2. 调用 self.reset() 清空历史，用新提示词重建 system 消息
      - 注意方法名是 set_system()，不是 set_system_prompt()

    这个测试：
      1. 创建一个客户端
      2. 调用 set_system("你是一个专业的翻译")
      3. 断言 system_prompt 属性已经更新
      4. 断言历史长度还是 1（reset 之后只有新的 system 消息）
    """
    client = LLMClient()
    client.set_system("你是一个专业的翻译")
    assert client.system_prompt == "你是一个专业的翻译"
    assert client.history_length == 1


# ══════════════════════════════════════════════════════════
# 测试 5：测试 chat() 方法，用 mock 模拟 API 调用
# ══════════════════════════════════════════════════════════
def test_chat_with_mock(mocker):
    """
    测试目标：在不真正调用 API 的情况下，验证 chat() 方法的逻辑。

    背景知识：
      - chat() 方法会调用真实的 API（需要网络和费用）
      - 用 mocker（pytest-mock 提供）可以"模拟"API 响应
      - 这样我们就能在不联网、不花钱的情况下测试 chat() 的逻辑
      - mocker.patch.object() 可以把真实对象的方法替换成假的

    什么是 Mock（模拟）？
      - Mock 是一个"假对象"，可以模拟真实对象的行为
      - 我们可以控制 Mock 返回什么值，然后检查代码是否正确处理了这些值
      - 这里我们模拟了 API 返回 "mocked reply"，然后检查：
        1. chat() 是否正确返回了这个值
        2. 历史记录是否更新了（user + assistant = 2 条新消息，
           加上原有的 1 条 system = 共 3 条）

    这个测试：
      1. 创建一个客户端
      2. 用 mocker.Mock() 创建一个模拟的 API 响应
      3. 把 client._client.chat.completions.create 替换成模拟函数
      4. 调用 client.chat("你好")
      5. 断言返回值是 "mocked reply"
      6. 断言历史长度变为 3（system + user + assistant）
    """
    client = LLMClient()

    # 创建一个 Mock 对象，模拟 API 的返回值
    mock_response = mocker.Mock()
    # API 响应结构：response.choices[0].message.content
    mock_response.choices = [mocker.Mock()]
    mock_response.choices[0].message.content = "mocked reply"

    # 替换真正的 API 调用，让它返回我们的模拟响应
    # 这样 chat() 方法就不会真的去调 API 了
    mocker.patch.object(
        client._client.chat.completions,
        "create",
        return_value=mock_response
    )

    # 调用 chat() 方法
    reply = client.chat("你好")

    # 验证返回值是模拟的 "mocked reply"
    assert reply == "mocked reply"
    # 验证历史记录现在有 3 条：system + user("你好") + assistant("mocked reply")
    assert client.history_length == 3