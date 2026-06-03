"""
LLMClient - 大模型客户端封装
功能：
1. 同步调用 + 流式调用
2. 多轮对话历史管理
3. 切换模型 / 温度 / system prompt
4. Token 计数与成本估算
"""

# 导入 dataclass 相关工具
from dataclasses import dataclass, field
# 导入类型标注
from typing import List, Optional, Generator
# 导入 OpenAI SDK
from openai import OpenAI
import os
# 导入 .env 文件读取工具
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量（API Key、地址等）
load_dotenv()


@dataclass
class ChatMessage:
    """单条对话消息的数据类"""
    role: str    # 消息角色："user"（用户） / "assistant"（AI） / "system"（系统指令）
    content: str # 消息内容

    def to_dict(self) -> dict:
        """将消息转换为 API 需要的字典格式"""
        return {"role": self.role, "content": self.content}


@dataclass
class LLMClient:
    """
    大模型客户端封装
    封装了与大模型 API 的交互逻辑，支持同步/流式调用和对话历史管理
    """

    # ---------- 字段定义（从 .env 读取配置） ----------
    # field(default_factory=lambda: ...) 确保每次创建实例时才读取环境变量
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    base_url: str = field(default_factory=lambda: os.getenv("OPENAI_API_BASE"))
    model: str = field(default_factory=lambda: os.getenv("MODEL"))
    temperature: float = field(default_factory=lambda: 0.7)  # 温度参数（0~1，越高越随机）
    system_prompt: str = "你是一个有帮助的AI助手"  # 系统提示词

    def __post_init__(self):
        """
        初始化后处理（dataclass 的特性，__init__ 执行完后自动调用）
        在这里创建 OpenAI 客户端实例和对话历史列表
        """
        # 创建 OpenAI 客户端（连接 LM Studio 本地 API）
        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        # 初始化对话历史列表
        self._history: List[ChatMessage] = []
        # 重置到初始状态（添加 system prompt）
        self.reset()

    def reset(self) -> None:
        """重置对话历史，只保留系统提示"""
        self._history = []
        self._history.append(ChatMessage(role="system", content=self.system_prompt))

    def set_system(self, prompt: str) -> None:
        """更换系统提示词并重置对话"""
        self.system_prompt = prompt
        self.reset()

    def chat(self, user_input: str) -> str:
        """
        同步调用大模型（等待全部回复后一次性返回）
        参数:
            user_input: 用户输入的文字
        返回:
            AI 回复的文字
        """
        # 1. 把用户消息加入历史
        self._history.append(ChatMessage(role="user", content=user_input))

        # 2. 调用 API（同步模式）
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[msg.to_dict() for msg in self._history],  # 把历史消息传给 AI
            temperature=self.temperature,
        )

        # 3. 从响应中提取 AI 回复
        reply = response.choices[0].message.content

        # 4. 把 AI 回复加入历史（保持对话记忆）
        self._history.append(ChatMessage(role="assistant", content=reply))

        return reply

    def stream_chat(self, user_input: str) -> Generator[str, None, None]:
        """
        流式调用大模型（逐字返回，打字机效果）
        参数:
            user_input: 用户输入的文字
        返回:
            生成器，每次 yield 一小段文字
        """
        # 1. 把用户消息加入历史
        self._history.append(ChatMessage(role="user", content=user_input))

        # 2. 调用 API（流式模式）
        stream = self._client.chat.completions.create(
            model=self.model,
            messages=[m.to_dict() for m in self._history],
            temperature=self.temperature,
            stream=True,  # 关键：开启流式
        )

        # 3. 逐块接收回复
        full_reply = ""
        for chunk in stream:
            # 每个 chunk 包含一小段文字
            delta = chunk.choices[0].delta.content
            if delta:
                full_reply += delta      # 累加完整回复
                yield delta              # 逐字返回（打字机效果）

        # 4. 把完整回复加入历史
        self._history.append(ChatMessage(role="assistant", content=full_reply))

    @property
    def history_length(self) -> int:
        """获取对话历史总条数（属性方式访问）"""
        return len(self._history)

    def show_history(self) -> None:
        """打印所有对话历史"""
        for i, msg in enumerate(self._history):
            # 只显示前 80 个字符，防止刷屏
            print(f"{i+1}. {msg.role}: {msg.content[:80]}")

    def get_history(self) -> List[ChatMessage]:
        """获取完整的对话历史列表"""
        return self._history