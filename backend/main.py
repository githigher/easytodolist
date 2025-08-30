# backend/main.py

import uvicorn  # 1. 导入uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.models import user, todo  # 关键：确保导入模型，以便create_all能找到它们
from app.routers import auth, todos

# 这行代码会根据你定义的模型，在数据库中创建对应的表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 配置CORS中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的前端源，根据你的Vue端口修改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do List API"}

# 2. 添加主程序入口
if __name__ == "__main__":
    uvicorn.run(
        "main:app",         # FastAPI实例的位置: "文件名:FastAPI实例名"
        host="127.0.0.1",   # 监听的IP地址
        port=8000,          # 监听的端口
        reload=True         # 启用代码热重载，与命令行--reload效果相同
    )