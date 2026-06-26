#!/bin/bash

# 经验工厂 - 启动脚本
# 同时启动后端 (:8000) 和前端 (:5173)

cleanup() {
    echo ""
    echo "正在停止服务..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "已停止"
}

trap cleanup EXIT INT TERM

echo "=== 经验工厂 ==="
echo "后端: http://localhost:8000"
echo "前端: http://localhost:5173"
echo ""

# 启动后端
uv run uvicorn backend.main:app --reload &
BACKEND_PID=$!

# 启动前端
cd frontend && npm run dev &
FRONTEND_PID=$!

echo "已启动，按 Ctrl+C 停止"
wait
