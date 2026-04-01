"""In-memory conversation history manager."""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import uuid
from app.core.logging import get_logger

logger = get_logger(__name__)

# Maximum number of message pairs (user + assistant) to keep per conversation
MAX_HISTORY_TURNS = 10
# Conversations expire after this many seconds of inactivity
CONVERSATION_TTL_SECONDS = 3600  # 1 hour


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class Conversation:
    id: str
    messages: List[Message] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)

    def add_user_message(self, content: str) -> None:
        self.messages.append(Message(role="user", content=content))
        self.last_active = time.time()

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(Message(role="assistant", content=content))
        self.last_active = time.time()

    def get_history_text(self) -> str:
        """Format history as text for injection into the LLM prompt."""
        if not self.messages:
            return ""

        # Keep only the last N turns (pairs of user+assistant)
        recent = self.messages[-(MAX_HISTORY_TURNS * 2):]
        lines = []
        for msg in recent:
            prefix = "User" if msg.role == "user" else "Assistant"
            lines.append(f"{prefix}: {msg.content}")
        return "\n".join(lines)

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.last_active) > CONVERSATION_TTL_SECONDS


class ConversationManager:
    """Thread-safe in-memory conversation store."""

    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}

    def get_or_create(self, conversation_id: Optional[str] = None) -> Conversation:
        """Get existing conversation or create a new one."""
        # Cleanup expired conversations periodically
        self._cleanup_expired()

        if conversation_id and conversation_id in self._conversations:
            conv = self._conversations[conversation_id]
            if not conv.is_expired:
                return conv
            else:
                logger.info("Conversation %s expired, creating new", conversation_id)
                del self._conversations[conversation_id]

        # Create new conversation
        new_id = conversation_id or uuid.uuid4().hex[:16]
        conv = Conversation(id=new_id)
        self._conversations[new_id] = conv
        logger.info("Created conversation %s (total active: %d)",
                    new_id, len(self._conversations))
        return conv

    def get(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID, returns None if not found or expired."""
        conv = self._conversations.get(conversation_id)
        if conv and not conv.is_expired:
            return conv
        return None

    def _cleanup_expired(self) -> None:
        """Remove expired conversations."""
        expired = [
            cid for cid, conv in self._conversations.items()
            if conv.is_expired
        ]
        for cid in expired:
            del self._conversations[cid]
        if expired:
            logger.info("Cleaned up %d expired conversations", len(expired))


# Global conversation manager instance
conversation_manager = ConversationManager()
