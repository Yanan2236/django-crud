from django.apps import AppConfig


class ShopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shops'
    verbose_name = 'ショップ管理'

    """
    def ready(self):
    
        アプリ起動時に一度だけ呼ばれる初期化処理。
        signalsを登録するのが主な使い方
        
        try:
            import guilds.signals
        except ImportError:
            pass
        """