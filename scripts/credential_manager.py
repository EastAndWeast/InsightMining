import os
import time

class CredentialManager:
    """
    凭据管理器：支持多 Key 轮询、状态监控及自动切换。
    """
    def __init__(self):
        self._load_dotenv()
        self.keys = {
            "GEMINI": self._load_keys("GEMINI_API_KEY"),
            "CANOPY": self._load_keys("CANOPY_API_KEY"),
            "OUTSCRAPER": self._load_keys("OUTSCRAPER_API_KEY")
        }
        self.status = {service: [True] * len(key_list) for service, key_list in self.keys.items()}
        self.last_failed = {service: [0] * len(key_list) for service, key_list in self.keys.items()}
        self.cooldown = 3600  # 失败后冷却 1 小时 (根据 API 限流策略调整)

    def _load_dotenv(self):
        """简单的 .env 加载器，避免依赖额外的库"""
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        os.environ[k] = v

    def _load_keys(self, env_prefix):
        """从环境变量加载多个 Key，格式如 GEMINI_API_KEY_1, GEMINI_API_KEY_2"""
        keys = []
        # 先尝试加载不带数字后缀的
        base_key = os.getenv(env_prefix)
        if base_key:
            keys.append(base_key)
        
        # 尝试加载带后缀的 (1-10)
        for i in range(1, 11):
            key = os.getenv(f"{env_prefix}_{i}")
            if key:
                keys.append(key)
        return keys

    def get_key(self, service):
        """获取当前可用的 Key"""
        service_keys = self.keys.get(service, [])
        if not service_keys:
            return None

        now = time.time()
        for i, key in enumerate(service_keys):
            # 检查是否在冷却中
            if not self.status[service][i]:
                if now - self.last_failed[service][i] > self.cooldown:
                    self.status[service][i] = True # 结束冷却
                else:
                    continue
            return key
        return None

    def mark_failed(self, service, key):
        """标记某个 Key 暂时不可用 (报错 429 或 401)"""
        if service in self.keys and key in self.keys[service]:
            idx = self.keys[service].index(key)
            self.status[service][idx] = False
            self.last_failed[service][idx] = time.time()
            print(f"WARNING: Key for {service} (Index {idx}) marked as FAILED. Switching to next...")

# 全局单例
credentials = CredentialManager()
