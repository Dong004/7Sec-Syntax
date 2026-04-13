@echo off
title Polyglot Rosetta Server
echo 正在唤醒本地数据库与大模型引擎...

:: 自动定位到当前脚本所在的文件夹 (防止路径找不到)
cd /d %~dp0

:: 自动激活你的 Anaconda 环境
call D:\PYTHON\Anaconda\Scripts\activate.bat base

:: 启动前端网页
streamlit run app.py