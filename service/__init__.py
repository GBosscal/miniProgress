from sanic import Sanic
from textwrap import dedent


def create_app():
    """
    创建APP例子，并且初始化APP
    :return: APP的实例
    """
    # 创建一个新的sanic应用
    app = Sanic("backend-for-pain-system")
    # 应用的健康检查配置
    app.config.HEALTH = True
    # 注册路由
    from view.user import user_blueprint
    from view.feedback import feedback_blueprint
    from view.stamp import stamp_blueprint
    from view.city import city_blueprint
    from view.point import point_blueprint
    from view.check_in import check_in_point_blueprint

    app.blueprint(user_blueprint)
    app.blueprint(feedback_blueprint)
    app.blueprint(stamp_blueprint)
    app.blueprint(city_blueprint)
    app.blueprint(point_blueprint)
    app.blueprint(check_in_point_blueprint)

    # 修改apidoc的定义
    app.ext.openapi.describe(
        "支付宝小程序",
        version="0.0.1",
        description=(
            """
            
            """
        )
    )

    return app
