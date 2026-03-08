"""配置模块单元测试"""

from traveler.config.settings import Settings, get_settings


def test_settings_defaults():
    """测试默认配置"""
    settings = Settings(
        _env_file=None, # type: ignore
        openai_api_key="test-key",
    )
    assert settings.app_name == "Traveler"
    assert settings.app_env == "development"
    assert settings.default_model_provider == "openai"
    assert not settings.is_production


def test_get_settings_singleton():
    """测试配置单例"""
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
