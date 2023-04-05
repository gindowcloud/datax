from pydantic import BaseModel


class ErrorBase(BaseModel):
    code: int
    message: str = None


# 找不到路径
ERROR_NOT_FOUND = ErrorBase(code=404, message="接口不存在")

# 参数错误
ERROR_PARAMETER_ERROR = ErrorBase(code=400, message="接口参数错误")

# 用户账户
ERROR_USER_TOKEN_EXPIRED = ErrorBase(code=10001, message="未登录或登录过期")
ERROR_USER_NOT_FOUND = ErrorBase(code=10002, message="用户账户错误")
ERROR_USER_WRONG_PASSWORD = ErrorBase(code=10003, message="用户密码错误")
ERROR_USER_CAPTCHA_ERROR = ErrorBase(code=10004, message="验证码错误")
ERROR_USER_USERNAME_EXIST = ErrorBase(code=10005, message="用户账户已被注册")
ERROR_USER_PHONE_EXIST = ErrorBase(code=10006, message="手机号码已被注册")
