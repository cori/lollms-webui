"""
project: lollms
file: lollms_discussion_events.py 
author: ParisNeo
description: 
    This module contains a set of Socketio routes that provide information about the Lord of Large Language and Multimodal Systems (LoLLMs) Web UI
    application. These routes are specific to discussion operation

"""
from fastapi import APIRouter, Request
from fastapi import HTTPException
from pydantic import BaseModel
import pkg_resources
from lollms.server.elf_server import LOLLMSElfServer
from fastapi.responses import FileResponse
from lollms.binding import BindingBuilder, InstallOption
from ascii_colors import ASCIIColors
from lollms.personality import MSG_TYPE, AIPersonality
from lollms.types import MSG_TYPE, SENDER_TYPES
from lollms.utilities import load_config, trace_exception, gc
from lollms.utilities import find_first_available_file_index, convert_language_name, PackageManager, run_async
from lollms_webui import LOLLMSWebUI
from pathlib import Path
from typing import List
from functools import partial
import socketio
import threading
import os
import time

from api.db import Discussion
from datetime import datetime

router = APIRouter()
lollmsElfServer:LOLLMSWebUI = LOLLMSWebUI.get_instance()


# ----------------------------------- events -----------------------------------------
def add_events(sio:socketio):
    @sio.on('start_webcam_video_stream')
    def start_webcam_video_stream(sid):
        lollmsElfServer.info("Starting video capture")
        lollmsElfServer.webcam.start_capture()

    @sio.on('stop_webcam_video_stream')
    def stop_webcam_video_stream(sid):
        lollmsElfServer.info("Stopping video capture")
        lollmsElfServer.webcam.stop_capture()

    @sio.on('start_audio_stream')
    def start_audio_stream(sid):
        lollmsElfServer.info("Starting audio capture")
        lollmsElfServer.audio_cap.start_recording()

    @sio.on('stop_audio_stream')
    def stop_audio_stream(sid):
        lollmsElfServer.info("Stopping audio capture")
        lollmsElfServer.audio_cap.stop_recording()

