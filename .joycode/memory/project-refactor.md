---
name: project-refactor
description: 2026-10后端架构重构：命名规范、拆分、统一依赖
type: project
---

后端重构完成(2026-10-11):
1. Application.py→app_factory.py(create_app工厂函数)
2. 统一main.py入口,删app/__main__.py
3. __init__.py仅__version__,无副作用
4. api/post.py拆为posts/comments/likes/categories
5. core/dependencies.py统一get_current_user_id
6. utils/security→core/security
7. database→infrastructure/database, redis_client→infrastructure/redis
8. response→responses, schemas/__init__.py改空

后续新增API按领域拆分,鉴权从core.dependencies导入