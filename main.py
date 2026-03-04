"""
TikTok Tools Telegram Bot
بوت تيليجرام لادارة حسابات تيك توك

Features:
- Delete all reposts from a TikTok account
- Download TikTok videos without watermark
- View account statistics
- Unlike all liked videos
- Search user info
- Extract video links from a profile
- Extract Session ID guide & helper
- Full Admin Panel for bot owner
"""

import os
import sys
import json
import asyncio
import logging
from typing import Optional
from datetime import datetime
from collections import defaultdict

# ─── Check dependencies ───────────────────────────────────────
try:
    import httpx
    from telegram import (
        Update,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        BotCommand,
    )
    from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        MessageHandler,
        ConversationHandler,
        ContextTypes,
        filters,
    )
except ImportError:
    print("Installing dependencies...")
    os.system(f"{sys.executable} -m pip install python-telegram-bot httpx")
    import httpx
    from telegram import (
        Update,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        BotCommand,
    )
    from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        MessageHandler,
        ConversationHandler,
        ContextTypes,
        filters,
    )


# ─── Logging Setup ────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─── Constants ─────────────────────────────────────────────────
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8528289566:AAEmPyaxSVBSiAMP9FTxOmKJnVXGzxZ_RGo")

# Set your Telegram user ID here to become the admin
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "5154904380"))

# Conversation states
WAITING_SESSION_ID = 1
WAITING_VIDEO_URL = 2
WAITING_USERNAME = 3
WAITING_EXTRACT_USERNAME = 4
WAITING_BROADCAST_MSG = 5
WAITING_BAN_USER_ID = 6

# TikTok API base URLs
TIKTOK_API_BASE = "https://www.tiktok.com/api"
TIKTOK_WEB_BASE = "https://www.tiktok.com"

# In-memory data stores
user_sessions: dict[int, dict] = {}
user_activity: dict[int, list] = defaultdict(list)
banned_users: set[int] = set()
bot_stats = {
    "start_time": datetime.now().isoformat(),
    "total_commands": 0,
    "total_downloads": 0,
    "total_reposts_deleted": 0,
    "total_unlikes": 0,
    "total_extracts": 0,
    "total_session_extracts": 0,
}


# ─── Helper: Admin Check ──────────────────────────────────────
def is_admin(user_id: int) -> bool:
    """Check if user is the bot admin."""
    return user_id == ADMIN_USER_ID


def is_banned(user_id: int) -> bool:
    """Check if user is banned."""
    return user_id in banned_users


def log_activity(user_id: int, action: str):
    """Log user activity for admin stats."""
    bot_stats["total_commands"] += 1
    user_activity[user_id].append(
        {"action": action, "time": datetime.now().isoformat()}
    )
    # Keep only the last 50 actions per user
    if len(user_activity[user_id]) > 50:
        user_activity[user_id] = user_activity[user_id][-50:]


# ─── TikTok API Helper Class ──────────────────────────────────
class TikTokAPI:
    """Helper class for TikTok API interactions."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.tiktok.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        }
        self.cookies = {"sessionid": session_id}

    async def get_user_info(self, username: Optional[str] = None) -> dict:
        """Fetch user profile information."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=30
        ) as client:
            if username:
                url = f"{TIKTOK_WEB_BASE}/@{username}"
            else:
                url = f"{TIKTOK_API_BASE}/user/detail/"

            try:
                resp = await client.get(url, follow_redirects=True)
                if resp.status_code == 200:
                    text = resp.text
                    if '"userInfo"' in text:
                        start = text.index('"userInfo"')
                        brace_count = 0
                        json_start = None
                        for i in range(start, len(text)):
                            if text[i] == "{":
                                if json_start is None:
                                    json_start = i
                                brace_count += 1
                            elif text[i] == "}":
                                brace_count -= 1
                                if brace_count == 0:
                                    try:
                                        data = json.loads(
                                            text[json_start : i + 1]
                                        )
                                        return {"success": True, "data": data}
                                    except json.JSONDecodeError:
                                        pass
                                    break
                return {"success": False, "error": "Could not fetch user info"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def get_user_videos(self, sec_uid: str, cursor: int = 0) -> dict:
        """Fetch user's video list."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=30
        ) as client:
            params = {
                "secUid": sec_uid,
                "count": 30,
                "cursor": cursor,
            }
            try:
                resp = await client.get(
                    f"{TIKTOK_API_BASE}/post/item_list/",
                    params=params,
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    return {"success": True, "data": resp.json()}
                return {"success": False, "error": f"Status: {resp.status_code}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def get_repost_list(self, cursor: int = 0) -> dict:
        """Fetch user's repost list."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=30
        ) as client:
            params = {
                "count": 30,
                "cursor": cursor,
            }
            try:
                resp = await client.get(
                    f"{TIKTOK_API_BASE}/repost/item_list/",
                    params=params,
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    return {"success": True, "data": resp.json()}
                return {"success": False, "error": f"Status: {resp.status_code}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def delete_repost(self, video_id: str) -> dict:
        """Remove a single repost."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=30
        ) as client:
            try:
                resp = await client.post(
                    f"{TIKTOK_API_BASE}/repost/delete/",
                    data={"itemId": video_id},
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    return {"success": True}
                return {"success": False, "error": f"Status: {resp.status_code}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def unlike_video(self, video_id: str) -> dict:
        """Unlike a single video."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=30
        ) as client:
            try:
                resp = await client.post(
                    f"{TIKTOK_API_BASE}/commit/item/digg/",
                    data={"itemId": video_id, "type": 0},
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    return {"success": True}
                return {"success": False, "error": f"Status: {resp.status_code}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def get_liked_videos(self, cursor: int = 0) -> dict:
        """Fetch user's liked videos."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=30
        ) as client:
            params = {
                "count": 30,
                "cursor": cursor,
            }
            try:
                resp = await client.get(
                    f"{TIKTOK_API_BASE}/favorite/item_list/",
                    params=params,
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    return {"success": True, "data": resp.json()}
                return {"success": False, "error": f"Status: {resp.status_code}"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def validate_session(self) -> dict:
        """Validate if the session ID is still active."""
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=15
        ) as client:
            try:
                resp = await client.get(
                    f"{TIKTOK_WEB_BASE}/api/user/detail/",
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("userInfo"):
                        return {
                            "success": True,
                            "valid": True,
                            "data": data["userInfo"],
                        }
                return {"success": True, "valid": False}
            except Exception as e:
                return {"success": False, "error": str(e)}


# ─── Download Helper ───────────────────────────────────────────
async def download_tiktok_video(url: str) -> dict:
    """Download a TikTok video without watermark using a public API."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            resp = await client.get(api_url, follow_redirects=True)

            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0 and data.get("data"):
                    video_data = data["data"]
                    download_url = video_data.get("play", "")
                    if download_url:
                        video_resp = await client.get(
                            download_url, follow_redirects=True
                        )
                        if video_resp.status_code == 200:
                            return {
                                "success": True,
                                "video_bytes": video_resp.content,
                                "title": video_data.get("title", "TikTok Video"),
                                "author": video_data.get("author", {}).get(
                                    "unique_id", "unknown"
                                ),
                                "stats": {
                                    "plays": video_data.get("play_count", 0),
                                    "likes": video_data.get("digg_count", 0),
                                    "comments": video_data.get(
                                        "comment_count", 0
                                    ),
                                    "shares": video_data.get("share_count", 0),
                                },
                            }

            return {"success": False, "error": "Could not download video"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ─── Format Helpers ────────────────────────────────────────────
def format_number(n: int) -> str:
    """Format large numbers for display."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def get_uptime() -> str:
    """Calculate bot uptime."""
    start = datetime.fromisoformat(bot_stats["start_time"])
    delta = datetime.now() - start
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    parts = []
    if days > 0:
        parts.append(f"{days} يوم")
    if hours > 0:
        parts.append(f"{hours} ساعة")
    parts.append(f"{minutes} دقيقة")
    return " و ".join(parts)


# ══════════════════════════════════════════════════════════════
#  BOT COMMAND HANDLERS
# ══════════════════════════════════════════════════════════════

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user

    if is_banned(user.id):
        await update.message.reply_text("⛔ تم حظرك من استخدام هذا البوت.")
        return

    log_activity(user.id, "start")
    is_logged_in = user.id in user_sessions

    welcome_text = (
        f"مرحبا {user.first_name}!\n\n"
        "🛠 *بوت ادوات تيك توك*\n\n"
        "بوت متقدم لادارة حسابك على تيك توك\n"
        "يوفر لك مجموعة ادوات قوية وسهلة الاستخدام.\n\n"
    )

    if is_logged_in:
        welcome_text += "✅ *حالة الحساب:* مسجل الدخول\n\n"
    else:
        welcome_text += "⚠️ *حالة الحساب:* غير مسجل\n\n"

    welcome_text += "اختر من القائمة ادناه:"

    keyboard = []

    if not is_logged_in:
        keyboard.append(
            [InlineKeyboardButton("🔐 تسجيل الدخول", callback_data="login")]
        )

    # Session ID extraction is always available (no login needed)
    keyboard.append(
        [InlineKeyboardButton("🔑 استخراج Session ID", callback_data="extract_session")]
    )

    if is_logged_in:
        keyboard.extend(
            [
                [
                    InlineKeyboardButton(
                        "🗑 حذف الريبوست", callback_data="delete_reposts"
                    ),
                    InlineKeyboardButton(
                        "📥 تحميل فيديو", callback_data="download_video"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📊 احصائياتي", callback_data="my_stats"
                    ),
                    InlineKeyboardButton(
                        "💔 ازالة الاعجابات", callback_data="unlike_all"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🔍 بحث مستخدم", callback_data="search_user"
                    ),
                    InlineKeyboardButton(
                        "🔗 استخراج روابط", callback_data="extract_links"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "✅ فحص الجلسة", callback_data="check_session"
                    ),
                    InlineKeyboardButton(
                        "🚪 تسجيل خروج", callback_data="logout"
                    ),
                ],
            ]
        )

    # Admin button (only visible to admin)
    if is_admin(user.id):
        keyboard.append(
            [
                InlineKeyboardButton(
                    "⚙️ لوحة الادمن", callback_data="admin_panel"
                )
            ]
        )

    keyboard.append(
        [InlineKeyboardButton("❓ المساعدة", callback_data="help")]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "📚 *دليل استخدام البوت*\n\n"
        "*الاوامر المتاحة:*\n"
        "▫️ /start - القائمة الرئيسية\n"
        "▫️ /login - تسجيل الدخول\n"
        "▫️ /session - استخراج Session ID\n"
        "▫️ /delete\\_reposts - حذف جميع الريبوست\n"
        "▫️ /download - تحميل فيديو\n"
        "▫️ /stats - احصائيات الحساب\n"
        "▫️ /unlike\\_all - ازالة جميع الاعجابات\n"
        "▫️ /user\\_info - بحث عن مستخدم\n"
        "▫️ /extract\\_links - استخراج روابط\n"
        "▫️ /check\\_session - فحص صلاحية الجلسة\n"
        "▫️ /logout - تسجيل الخروج\n"
        "▫️ /help - هذه القائمة\n\n"
        "*كيف احصل على Session ID؟*\n"
        "استخدم امر /session للحصول على شرح تفصيلي مع صور.\n\n"
        "⚠️ *تنبيه:* لا تشارك Session ID مع اي شخص!"
    )

    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            help_text, parse_mode="Markdown"
        )


# ══════════════════════════════════════════════════════════════
#  SESSION ID EXTRACTION GUIDE
# ══════════════════════════════════════════════════════════════

async def session_extract_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show detailed Session ID extraction guide."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if is_banned(user.id):
        await msg.reply_text("⛔ تم حظرك من استخدام هذا البوت.")
        return

    log_activity(user.id, "extract_session")
    bot_stats["total_session_extracts"] += 1

    guide_text = (
        "🔑 *دليل استخراج Session ID*\n\n"
        "Session ID هو مفتاح الجلسة الذي يسمح للبوت بالتعامل مع حسابك.\n"
        "اتبع الخطوات التالية بدقة:\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "*الطريقة 1: من المتصفح (كمبيوتر)*\n\n"
        "1️⃣ افتح المتصفح (Chrome / Firefox / Edge)\n"
        "2️⃣ اذهب الى tiktok.com وسجل دخولك\n"
        "3️⃣ اضغط F12 لفتح ادوات المطور\n"
        "4️⃣ اختر تبويب *Application* (في Chrome)\n"
        "    او *Storage* (في Firefox)\n"
        "5️⃣ من القائمة الجانبية اختر:\n"
        "    Cookies > https://www.tiktok.com\n"
        "6️⃣ ابحث عن `sessionid` في القائمة\n"
        "7️⃣ انقر عليها مرتين وانسخ *القيمة* كاملة\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "*الطريقة 2: من المتصفح (جوال)*\n\n"
        "1️⃣ افتح متصفح Chrome على الجوال\n"
        "2️⃣ اذهب الى tiktok.com وسجل دخولك\n"
        "3️⃣ في شريط العنوان اكتب:\n"
        "    `javascript:document.cookie`\n"
        "4️⃣ او استخدم اضافة Cookie Editor\n"
        "5️⃣ ابحث عن sessionid وانسخ قيمتها\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "*الطريقة 3: استخدام اضافة المتصفح*\n\n"
        "1️⃣ ثبت اضافة *EditThisCookie* او *Cookie Editor*\n"
        "    من متجر اضافات Chrome\n"
        "2️⃣ اذهب الى tiktok.com\n"
        "3️⃣ اضغط على ايقونة الاضافة\n"
        "4️⃣ ابحث عن `sessionid`\n"
        "5️⃣ انسخ القيمة\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "*الطريقة 4: باستخدام كود JavaScript*\n\n"
        "1️⃣ افتح tiktok.com وسجل دخولك\n"
        "2️⃣ اضغط F12 واذهب لتبويب Console\n"
        "3️⃣ الصق هذا الكود واضغط Enter:\n\n"
    )

    await msg.reply_text(guide_text, parse_mode="Markdown")

    # Send the JavaScript code separately for easy copying
    js_code = (
        "```javascript\n"
        "// استخراج Session ID\n"
        "const cookies = document.cookie.split(';');\n"
        "const sessionCookie = cookies.find(\n"
        "  c => c.trim().startsWith('sessionid=')\n"
        ");\n"
        "if (sessionCookie) {\n"
        "  const sid = sessionCookie.split('=')[1];\n"
        "  console.log('Session ID:', sid);\n"
        "  // نسخ تلقائي\n"
        "  navigator.clipboard.writeText(sid)\n"
        "    .then(() => alert('تم نسخ Session ID!'))\n"
        "    .catch(() => prompt('انسخ يدويا:', sid));\n"
        "} else {\n"
        "  alert('لم يتم العثور على sessionid! تأكد من تسجيل الدخول');\n"
        "}\n"
        "```"
    )

    await msg.reply_text(js_code, parse_mode="Markdown")

    # Tips message
    tips_text = (
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚠️ *تنبيهات مهمة:*\n\n"
        "• لا تشارك Session ID مع اي شخص\n"
        "• Session ID تنتهي صلاحيته بعد فترة\n"
        "• اذا غيرت كلمة المرور يتغير Session ID\n"
        "• البوت يحذف رسالة Session ID تلقائيا لحمايتك\n"
        "• يمكنك فحص صلاحية الجلسة بامر /check\\_session\n\n"
        "بعد نسخ Session ID، استخدم /login لتسجيل الدخول."
    )

    keyboard = [
        [InlineKeyboardButton("🔐 تسجيل الدخول الان", callback_data="login")],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_start")],
    ]

    await msg.reply_text(
        tips_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ─── Check Session Validity ───────────────────────────────────
async def check_session_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Check if current session is still valid."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if user.id not in user_sessions:
        await msg.reply_text(
            "⚠️ يجب تسجيل الدخول اولا.\nاستخدم /login"
        )
        return

    log_activity(user.id, "check_session")

    status_msg = await msg.reply_text(
        "🔄 *جاري فحص صلاحية الجلسة...*", parse_mode="Markdown"
    )

    session_id = user_sessions[user.id]["session_id"]
    api = TikTokAPI(session_id)
    result = await api.validate_session()

    if result.get("success") and result.get("valid"):
        user_data = result.get("data", {}).get("user", {})
        nickname = user_data.get("nickname", "غير معروف")
        unique_id = user_data.get("uniqueId", "غير معروف")

        # Calculate session age
        login_time = user_sessions[user.id].get("login_time", "")
        if login_time:
            login_dt = datetime.fromisoformat(login_time)
            age = datetime.now() - login_dt
            age_str = f"{age.days} يوم و {age.seconds // 3600} ساعة"
        else:
            age_str = "غير معروف"

        await status_msg.edit_text(
            f"✅ *الجلسة صالحة!*\n\n"
            f"👤 *الحساب:* {nickname} (@{unique_id})\n"
            f"⏱ *عمر الجلسة:* {age_str}\n"
            f"🟢 *الحالة:* نشطة ومتصلة",
            parse_mode="Markdown",
        )
    else:
        await status_msg.edit_text(
            "❌ *الجلسة منتهية الصلاحية!*\n\n"
            "يجب اعادة تسجيل الدخول بـ Session ID جديد.\n"
            "استخدم /session للحصول على الدليل.\n"
            "ثم استخدم /login لتسجيل الدخول.",
            parse_mode="Markdown",
        )


# ─── Login Flow ────────────────────────────────────────────────
async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start login flow."""
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    text = (
        "🔐 *تسجيل الدخول*\n\n"
        "لربط حسابك، ارسل لي *Session ID* الخاص بحسابك على تيك توك.\n\n"
        "*لا تعرف كيف تحصل عليه؟*\n"
        "استخدم /session لعرض الدليل الكامل.\n\n"
        "ارسل Session ID الان:"
    )

    await msg.reply_text(text, parse_mode="Markdown")
    return WAITING_SESSION_ID


async def receive_session_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Process received session ID."""
    user = update.effective_user
    session_id = update.message.text.strip()

    # Basic validation
    if len(session_id) < 20:
        await update.message.reply_text(
            "❌ Session ID غير صالح. يجب ان يكون اطول من 20 حرف.\n"
            "حاول مرة اخرى او اضغط /start للرجوع."
        )
        return WAITING_SESSION_ID

    # Store session
    user_sessions[user.id] = {
        "session_id": session_id,
        "login_time": datetime.now().isoformat(),
        "user_name": user.first_name,
        "user_id": user.id,
        "username": user.username or "N/A",
    }

    log_activity(user.id, "login")

    # Delete the message containing session ID for security
    try:
        await update.message.delete()
    except Exception:
        pass

    await update.message.reply_text(
        "✅ *تم تسجيل الدخول بنجاح!*\n\n"
        "تم حذف رسالتك لحماية بياناتك.\n"
        "استخدم /check\\_session للتاكد من الصلاحية.\n"
        "اضغط /start لعرض القائمة الرئيسية.",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


# ─── Logout ────────────────────────────────────────────────────
async def logout_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle logout."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if user.id in user_sessions:
        del user_sessions[user.id]
        log_activity(user.id, "logout")
        await msg.reply_text(
            "✅ تم تسجيل الخروج بنجاح وحذف جميع بياناتك.\n"
            "اضغط /start للعودة."
        )
    else:
        await msg.reply_text("⚠️ انت غير مسجل دخول اصلا.")


# ─── Delete Reposts ────────────────────────────────────────────
async def delete_reposts_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle delete reposts command."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if is_banned(user.id):
        await msg.reply_text("⛔ تم حظرك من استخدام هذا البوت.")
        return

    if user.id not in user_sessions:
        await msg.reply_text(
            "⚠️ يجب تسجيل الدخول اولا.\nاستخدم /login"
        )
        return

    log_activity(user.id, "delete_reposts")
    session_id = user_sessions[user.id]["session_id"]
    api = TikTokAPI(session_id)

    status_msg = await msg.reply_text(
        "🔄 *جاري جلب الريبوست...*", parse_mode="Markdown"
    )

    total_deleted = 0
    cursor = 0
    has_more = True

    while has_more:
        result = await api.get_repost_list(cursor)

        if not result["success"]:
            await status_msg.edit_text(
                f"❌ حدث خطا: {result['error']}\n\n"
                "تاكد من صلاحية Session ID."
            )
            return

        data = result.get("data", {})
        items = data.get("itemList", data.get("item_list", []))

        if not items:
            break

        has_more = data.get("hasMore", False)
        cursor = data.get("cursor", 0)

        for item in items:
            video_id = item.get("id", item.get("video", {}).get("id", ""))
            if video_id:
                del_result = await api.delete_repost(video_id)
                if del_result["success"]:
                    total_deleted += 1

                if total_deleted % 5 == 0:
                    try:
                        await status_msg.edit_text(
                            f"🔄 *جاري الحذف...*\n"
                            f"تم حذف: {total_deleted} ريبوست",
                            parse_mode="Markdown",
                        )
                    except Exception:
                        pass

                await asyncio.sleep(0.5)

    bot_stats["total_reposts_deleted"] += total_deleted
    await status_msg.edit_text(
        f"✅ *تم الانتهاء!*\n\n"
        f"تم حذف *{total_deleted}* ريبوست بنجاح.",
        parse_mode="Markdown",
    )


# ─── Download Video ────────────────────────────────────────────
async def download_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Start download flow."""
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    await msg.reply_text(
        "📥 *تحميل فيديو تيك توك*\n\n"
        "ارسل رابط الفيديو الذي تريد تحميله:",
        parse_mode="Markdown",
    )
    return WAITING_VIDEO_URL


async def receive_video_url(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Process video URL and download."""
    url = update.message.text.strip()

    if "tiktok.com" not in url and "vm.tiktok.com" not in url:
        await update.message.reply_text(
            "❌ الرابط غير صالح. ارسل رابط تيك توك صحيح."
        )
        return WAITING_VIDEO_URL

    log_activity(update.effective_user.id, "download")

    status_msg = await update.message.reply_text(
        "🔄 *جاري التحميل...*", parse_mode="Markdown"
    )

    result = await download_tiktok_video(url)

    if result["success"]:
        video_bytes = result["video_bytes"]
        caption = (
            f"📹 *{result['title'][:100]}*\n"
            f"👤 @{result['author']}\n\n"
            f"👁 {format_number(result['stats']['plays'])} مشاهدة | "
            f"❤️ {format_number(result['stats']['likes'])} اعجاب | "
            f"💬 {format_number(result['stats']['comments'])} تعليق"
        )

        try:
            await status_msg.delete()
        except Exception:
            pass

        from io import BytesIO

        video_file = BytesIO(video_bytes)
        video_file.name = "tiktok_video.mp4"

        await update.message.reply_video(
            video=video_file,
            caption=caption,
            parse_mode="Markdown",
            supports_streaming=True,
        )
        bot_stats["total_downloads"] += 1
    else:
        await status_msg.edit_text(f"❌ فشل التحميل: {result['error']}")

    return ConversationHandler.END


# ─── Account Stats ─────────────────────────────────────────────
async def stats_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show account statistics."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if user.id not in user_sessions:
        await msg.reply_text(
            "⚠️ يجب تسجيل الدخول اولا.\nاستخدم /login"
        )
        return

    log_activity(user.id, "stats")
    session_id = user_sessions[user.id]["session_id"]
    api = TikTokAPI(session_id)

    status_msg = await msg.reply_text(
        "🔄 *جاري جلب الاحصائيات...*", parse_mode="Markdown"
    )

    result = await api.get_user_info()

    if result["success"]:
        data = result["data"]
        user_data = data.get("user", {})
        stats_data = data.get("stats", {})

        nickname = user_data.get("nickname", "غير معروف")
        unique_id = user_data.get("uniqueId", "غير معروف")
        bio = user_data.get("signature", "لا يوجد")
        verified = "✅" if user_data.get("verified", False) else "❌"
        private = "🔒 خاص" if user_data.get("privateAccount", False) else "🌐 عام"

        followers = format_number(stats_data.get("followerCount", 0))
        following = format_number(stats_data.get("followingCount", 0))
        likes = format_number(stats_data.get("heartCount", 0))
        videos = format_number(stats_data.get("videoCount", 0))

        stats_text = (
            f"📊 *احصائيات الحساب*\n\n"
            f"👤 *الاسم:* {nickname}\n"
            f"🆔 *المعرف:* @{unique_id}\n"
            f"✍️ *البايو:* {bio[:100]}\n"
            f"☑️ *موثق:* {verified}\n"
            f"🔐 *الخصوصية:* {private}\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👥 *المتابعون:* {followers}\n"
            f"👤 *المتابَعون:* {following}\n"
            f"❤️ *الاعجابات:* {likes}\n"
            f"🎬 *الفيديوهات:* {videos}\n"
        )

        await status_msg.edit_text(stats_text, parse_mode="Markdown")
    else:
        await status_msg.edit_text(
            f"❌ حدث خطا: {result['error']}\n"
            "تاكد من صلاحية Session ID."
        )


# ─── Unlike All ────────────────────────────────────────────────
async def unlike_all_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Remove all likes."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if user.id not in user_sessions:
        await msg.reply_text(
            "⚠️ يجب تسجيل الدخول اولا.\nاستخدم /login"
        )
        return

    log_activity(user.id, "unlike_all")

    keyboard = [
        [
            InlineKeyboardButton("✅ نعم، احذف الكل", callback_data="confirm_unlike"),
            InlineKeyboardButton("❌ الغاء", callback_data="cancel_unlike"),
        ]
    ]
    await msg.reply_text(
        "⚠️ *تحذير!*\n\n"
        "هل انت متاكد من ازالة جميع الاعجابات؟\n"
        "هذا الاجراء لا يمكن التراجع عنه!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def confirm_unlike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Execute unlike all after confirmation."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    session_id = user_sessions[user.id]["session_id"]
    api = TikTokAPI(session_id)

    status_msg = await query.message.reply_text(
        "🔄 *جاري ازالة الاعجابات...*", parse_mode="Markdown"
    )

    total_unliked = 0
    cursor = 0
    has_more = True

    while has_more:
        result = await api.get_liked_videos(cursor)

        if not result["success"]:
            await status_msg.edit_text(
                f"❌ حدث خطا: {result['error']}"
            )
            return

        data = result.get("data", {})
        items = data.get("itemList", data.get("item_list", []))

        if not items:
            break

        has_more = data.get("hasMore", False)
        cursor = data.get("cursor", 0)

        for item in items:
            video_id = item.get("id", "")
            if video_id:
                unlike_result = await api.unlike_video(video_id)
                if unlike_result["success"]:
                    total_unliked += 1

                if total_unliked % 10 == 0:
                    try:
                        await status_msg.edit_text(
                            f"🔄 *جاري الازالة...*\n"
                            f"تم ازالة: {total_unliked} اعجاب",
                            parse_mode="Markdown",
                        )
                    except Exception:
                        pass

                await asyncio.sleep(0.3)

    bot_stats["total_unlikes"] += total_unliked
    await status_msg.edit_text(
        f"✅ *تم الانتهاء!*\n\n"
        f"تم ازالة *{total_unliked}* اعجاب.",
        parse_mode="Markdown",
    )


async def cancel_unlike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel unlike operation."""
    query = update.callback_query
    await query.answer()
    await query.message.edit_text("❌ تم الغاء العملية.")


# ─── Search User ───────────────────────────────────────────────
async def search_user_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Start user search flow."""
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    await msg.reply_text(
        "🔍 *البحث عن مستخدم*\n\n"
        "ارسل اسم المستخدم (بدون @):",
        parse_mode="Markdown",
    )
    return WAITING_USERNAME


async def receive_username(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Process username search."""
    username = update.message.text.strip().replace("@", "")

    log_activity(update.effective_user.id, "search_user")

    status_msg = await update.message.reply_text(
        f"🔍 *جاري البحث عن @{username}...*",
        parse_mode="Markdown",
    )

    api = TikTokAPI("")
    result = await api.get_user_info(username)

    if result["success"]:
        data = result["data"]
        user_data = data.get("user", {})
        stats_data = data.get("stats", {})

        nickname = user_data.get("nickname", "غير معروف")
        bio = user_data.get("signature", "لا يوجد")
        verified = "✅" if user_data.get("verified", False) else "❌"

        followers = format_number(stats_data.get("followerCount", 0))
        following = format_number(stats_data.get("followingCount", 0))
        likes = format_number(stats_data.get("heartCount", 0))
        videos = format_number(stats_data.get("videoCount", 0))

        info_text = (
            f"👤 *معلومات @{username}*\n\n"
            f"📛 *الاسم:* {nickname}\n"
            f"✍️ *البايو:* {bio[:100]}\n"
            f"☑️ *موثق:* {verified}\n\n"
            f"👥 المتابعون: {followers}\n"
            f"👤 المتابَعون: {following}\n"
            f"❤️ الاعجابات: {likes}\n"
            f"🎬 الفيديوهات: {videos}\n"
        )

        await status_msg.edit_text(info_text, parse_mode="Markdown")
    else:
        await status_msg.edit_text(
            f"❌ لم يتم العثور على المستخدم @{username}"
        )

    return ConversationHandler.END


# ─── Extract Links ─────────────────────────────────────────────
async def extract_links_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Start extract links flow."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if user.id not in user_sessions:
        await msg.reply_text(
            "⚠️ يجب تسجيل الدخول اولا.\nاستخدم /login"
        )
        return ConversationHandler.END

    await msg.reply_text(
        "🔗 *استخراج الروابط*\n\n"
        "ارسل اسم المستخدم الذي تريد استخراج روابط فيديوهاته (بدون @):",
        parse_mode="Markdown",
    )
    return WAITING_EXTRACT_USERNAME


async def receive_extract_username(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Process extract links for a user."""
    user = update.effective_user
    username = update.message.text.strip().replace("@", "")

    log_activity(user.id, "extract_links")
    bot_stats["total_extracts"] += 1

    status_msg = await update.message.reply_text(
        f"🔄 *جاري استخراج روابط @{username}...*",
        parse_mode="Markdown",
    )

    session_id = user_sessions[user.id]["session_id"]
    api = TikTokAPI(session_id)

    user_result = await api.get_user_info(username)

    if not user_result["success"]:
        await status_msg.edit_text(
            f"❌ لم يتم العثور على @{username}"
        )
        return ConversationHandler.END

    sec_uid = user_result["data"].get("user", {}).get("secUid", "")
    if not sec_uid:
        await status_msg.edit_text("❌ لم يتم العثور على معرف المستخدم.")
        return ConversationHandler.END

    links = []
    cursor = 0
    has_more = True

    while has_more and len(links) < 200:
        result = await api.get_user_videos(sec_uid, cursor)

        if not result["success"]:
            break

        data = result.get("data", {})
        items = data.get("itemList", data.get("item_list", []))

        if not items:
            break

        has_more = data.get("hasMore", False)
        cursor = data.get("cursor", 0)

        for item in items:
            video_id = item.get("id", "")
            if video_id:
                links.append(
                    f"https://www.tiktok.com/@{username}/video/{video_id}"
                )

        await asyncio.sleep(0.5)

    if links:
        links_text = "\n".join(links)
        header = f"🔗 *روابط فيديوهات @{username}*\nالعدد: {len(links)}\n\n"

        if len(header + links_text) > 4000:
            from io import BytesIO

            file = BytesIO(links_text.encode("utf-8"))
            file.name = f"{username}_links.txt"

            await status_msg.delete()
            await update.message.reply_document(
                document=file,
                caption=f"🔗 تم استخراج {len(links)} رابط لـ @{username}",
            )
        else:
            await status_msg.edit_text(
                header + links_text, parse_mode="Markdown"
            )
    else:
        await status_msg.edit_text(
            f"❌ لم يتم العثور على فيديوهات لـ @{username}"
        )

    return ConversationHandler.END


# ══════════════════════════════════════════════════════════════
#  ADMIN PANEL
# ══════════════════════════════════════════════════════════════

async def admin_panel_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show admin panel - only for bot owner."""
    user = update.effective_user
    msg = update.message or (update.callback_query.message if update.callback_query else None)
    if not msg:
        return

    if not is_admin(user.id):
        await msg.reply_text("⛔ ليس لديك صلاحية للوصول الى لوحة الادمن.")
        return

    keyboard = [
        [
            InlineKeyboardButton("📊 احصائيات البوت", callback_data="admin_stats"),
            InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users"),
        ],
        [
            InlineKeyboardButton("🟢 الجلسات النشطة", callback_data="admin_sessions"),
            InlineKeyboardButton("📋 سجل النشاط", callback_data="admin_activity"),
        ],
        [
            InlineKeyboardButton("📢 اذاعة رسالة", callback_data="admin_broadcast"),
            InlineKeyboardButton("🚫 حظر مستخدم", callback_data="admin_ban"),
        ],
        [
            InlineKeyboardButton("✅ الغاء حظر", callback_data="admin_unban"),
            InlineKeyboardButton("📜 قائمة المحظورين", callback_data="admin_banned_list"),
        ],
        [
            InlineKeyboardButton("🔄 اعادة تشغيل", callback_data="admin_restart"),
            InlineKeyboardButton("🗑 مسح البيانات", callback_data="admin_clear_data"),
        ],
        [
            InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_start"),
        ],
    ]

    admin_text = (
        "⚙️ *لوحة تحكم الادمن*\n\n"
        f"👤 *المسؤول:* {user.first_name}\n"
        f"🆔 *الـ ID:* `{user.id}`\n"
        f"⏱ *وقت التشغيل:* {get_uptime()}\n"
        f"👥 *المستخدمين النشطين:* {len(user_sessions)}\n"
        f"🚫 *المحظورين:* {len(banned_users)}\n\n"
        "اختر من الخيارات ادناه:"
    )

    await msg.reply_text(
        admin_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_stats_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show detailed bot statistics."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    stats_text = (
        "📊 *احصائيات البوت التفصيلية*\n\n"
        f"⏱ *وقت التشغيل:* {get_uptime()}\n"
        f"📅 *تاريخ البدء:* {bot_stats['start_time'][:19]}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📈 *احصائيات الاستخدام:*\n"
        f"▫️ اجمالي الاوامر: {bot_stats['total_commands']}\n"
        f"▫️ التحميلات: {bot_stats['total_downloads']}\n"
        f"▫️ الريبوست المحذوف: {bot_stats['total_reposts_deleted']}\n"
        f"▫️ الاعجابات المزالة: {bot_stats['total_unlikes']}\n"
        f"▫️ استخراج الروابط: {bot_stats['total_extracts']}\n"
        f"▫️ استخراج Session ID: {bot_stats['total_session_extracts']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 *المستخدمين:*\n"
        f"▫️ مسجلي الدخول: {len(user_sessions)}\n"
        f"▫️ المحظورين: {len(banned_users)}\n"
        f"▫️ اجمالي المتفاعلين: {len(user_activity)}\n"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 لوحة الادمن", callback_data="admin_panel")]
    ]

    await query.message.reply_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_users_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """List all registered users."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    if not user_sessions:
        await query.message.reply_text("📭 لا يوجد مستخدمين مسجلين حاليا.")
        return

    users_text = "👥 *المستخدمين المسجلين:*\n\n"

    for uid, data in user_sessions.items():
        name = data.get("user_name", "غير معروف")
        username = data.get("username", "N/A")
        login_time = data.get("login_time", "")[:19]
        session_preview = data.get("session_id", "")[:8] + "..."

        users_text += (
            f"▫️ *{name}* (@{username})\n"
            f"   ID: `{uid}`\n"
            f"   الدخول: {login_time}\n"
            f"   الجلسة: `{session_preview}`\n\n"
        )

    keyboard = [
        [InlineKeyboardButton("🔙 لوحة الادمن", callback_data="admin_panel")]
    ]

    # Truncate if too long
    if len(users_text) > 4000:
        users_text = users_text[:3900] + "\n\n... وغيرهم"

    await query.message.reply_text(
        users_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_sessions_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show active sessions details."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    if not user_sessions:
        await query.message.reply_text("📭 لا توجد جلسات نشطة.")
        return

    sessions_text = "🟢 *الجلسات النشطة:*\n\n"

    for uid, data in user_sessions.items():
        name = data.get("user_name", "غير معروف")
        login_time = data.get("login_time", "")
        if login_time:
            login_dt = datetime.fromisoformat(login_time)
            age = datetime.now() - login_dt
            age_str = f"{age.days}d {age.seconds // 3600}h"
        else:
            age_str = "N/A"

        activity_count = len(user_activity.get(uid, []))

        sessions_text += (
            f"▫️ *{name}* (ID: `{uid}`)\n"
            f"   العمر: {age_str} | الاوامر: {activity_count}\n\n"
        )

    keyboard = [
        [InlineKeyboardButton("🔙 لوحة الادمن", callback_data="admin_panel")]
    ]

    await query.message.reply_text(
        sessions_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_activity_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show recent activity log."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    # Collect all activities and sort by time
    all_activities = []
    for uid, activities in user_activity.items():
        name = user_sessions.get(uid, {}).get("user_name", str(uid))
        for act in activities[-10:]:  # Last 10 per user
            all_activities.append(
                {
                    "user": name,
                    "user_id": uid,
                    "action": act["action"],
                    "time": act["time"],
                }
            )

    all_activities.sort(key=lambda x: x["time"], reverse=True)
    recent = all_activities[:30]

    if not recent:
        await query.message.reply_text("📭 لا يوجد نشاط مسجل.")
        return

    activity_text = "📋 *سجل النشاط (اخر 30):*\n\n"

    action_names = {
        "start": "بدء",
        "login": "تسجيل دخول",
        "logout": "تسجيل خروج",
        "delete_reposts": "حذف ريبوست",
        "download": "تحميل",
        "stats": "احصائيات",
        "unlike_all": "ازالة اعجابات",
        "search_user": "بحث مستخدم",
        "extract_links": "استخراج روابط",
        "extract_session": "استخراج جلسة",
        "check_session": "فحص جلسة",
    }

    for act in recent:
        time_str = act["time"][11:19]
        action_name = action_names.get(act["action"], act["action"])
        activity_text += f"▫️ `{time_str}` | *{act['user']}* | {action_name}\n"

    keyboard = [
        [InlineKeyboardButton("🔙 لوحة الادمن", callback_data="admin_panel")]
    ]

    await query.message.reply_text(
        activity_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_broadcast_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Start broadcast message flow."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    total_users = len(user_activity)
    await query.message.reply_text(
        f"📢 *اذاعة رسالة*\n\n"
        f"سيتم ارسال الرسالة لـ {total_users} مستخدم.\n"
        f"اكتب الرسالة التي تريد ارسالها:\n\n"
        f"(ارسل /cancel للالغاء)",
        parse_mode="Markdown",
    )
    return WAITING_BROADCAST_MSG


async def receive_broadcast_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Send broadcast message to all known users."""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END

    message = update.message.text
    sent = 0
    failed = 0

    status_msg = await update.message.reply_text(
        "🔄 *جاري الارسال...*", parse_mode="Markdown"
    )

    for uid in user_activity.keys():
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"📢 *رسالة من الادارة:*\n\n{message}",
                parse_mode="Markdown",
            )
            sent += 1
        except Exception:
            failed += 1

        await asyncio.sleep(0.1)  # Rate limit

    await status_msg.edit_text(
        f"✅ *تم الارسال!*\n\n"
        f"▫️ تم الارسال: {sent}\n"
        f"▫️ فشل: {failed}",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def admin_ban_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Start ban user flow."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    await query.message.reply_text(
        "🚫 *حظر مستخدم*\n\n"
        "ارسل الـ User ID للمستخدم الذي تريد حظره:\n\n"
        "(ارسل /cancel للالغاء)",
        parse_mode="Markdown",
    )
    return WAITING_BAN_USER_ID


async def receive_ban_user_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Process ban request."""
    if not is_admin(update.effective_user.id):
        return ConversationHandler.END

    try:
        target_id = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("❌ يرجى ارسال رقم صحيح.")
        return WAITING_BAN_USER_ID

    if target_id == ADMIN_USER_ID:
        await update.message.reply_text("❌ لا يمكنك حظر نفسك!")
        return ConversationHandler.END

    banned_users.add(target_id)

    # Remove their session if they have one
    if target_id in user_sessions:
        del user_sessions[target_id]

    # Try to notify the banned user
    try:
        await context.bot.send_message(
            chat_id=target_id,
            text="⛔ تم حظرك من استخدام هذا البوت من قبل الادارة.",
        )
    except Exception:
        pass

    await update.message.reply_text(
        f"✅ تم حظر المستخدم `{target_id}` بنجاح.\n"
        "تم حذف جلسته ان وجدت.",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def admin_unban_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Unban a user."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    if not banned_users:
        await query.message.reply_text("📭 لا يوجد مستخدمين محظورين.")
        return

    # Create buttons for each banned user
    keyboard = []
    for uid in banned_users:
        name = user_activity.get(uid, [{}])
        keyboard.append(
            [InlineKeyboardButton(f"✅ الغاء حظر {uid}", callback_data=f"do_unban_{uid}")]
        )

    keyboard.append(
        [InlineKeyboardButton("🔙 لوحة الادمن", callback_data="admin_panel")]
    )

    await query.message.reply_text(
        "✅ *الغاء حظر مستخدم*\n\nاختر المستخدم:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_banned_list_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show list of banned users."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    if not banned_users:
        await query.message.reply_text("📭 لا يوجد مستخدمين محظورين.")
        return

    text = "📜 *قائمة المحظورين:*\n\n"
    for uid in banned_users:
        text += f"▫️ `{uid}`\n"

    keyboard = [
        [InlineKeyboardButton("🔙 لوحة الادمن", callback_data="admin_panel")]
    ]

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_clear_data_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Clear all bot data with confirmation."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    keyboard = [
        [
            InlineKeyboardButton("✅ نعم، امسح الكل", callback_data="confirm_clear"),
            InlineKeyboardButton("❌ الغاء", callback_data="admin_panel"),
        ]
    ]

    await query.message.reply_text(
        "⚠️ *تحذير خطير!*\n\n"
        "هذا سيحذف:\n"
        "▫️ جميع الجلسات النشطة\n"
        "▫️ سجل النشاط\n"
        "▫️ احصائيات الاستخدام\n\n"
        "هل انت متاكد؟",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def admin_restart_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Restart confirmation."""
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    keyboard = [
        [
            InlineKeyboardButton("✅ اعادة تشغيل", callback_data="confirm_restart"),
            InlineKeyboardButton("❌ الغاء", callback_data="admin_panel"),
        ]
    ]

    await query.message.reply_text(
        "🔄 *اعادة تشغيل البوت*\n\n"
        "سيتم اعادة ضبط جميع الجلسات.\n"
        "هل انت متاكد؟",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


# ─── Callback Query Handler ────────────────────────────────────
async def button_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle button presses from inline keyboard."""
    query = update.callback_query
    await query.answer()

    data = query.data
    user = update.effective_user

    # ─── User Actions ─────────────────
    if data == "login":
        await query.message.reply_text(
            "🔐 *تسجيل الدخول*\n\n"
            "ارسل لي Session ID الخاص بحسابك:\n"
            "(استخدم /session لمعرفة كيف تحصل عليه)",
            parse_mode="Markdown",
        )
    elif data == "extract_session":
        await session_extract_command(update, context)
    elif data == "check_session":
        await check_session_command(update, context)
    elif data == "delete_reposts":
        await delete_reposts_command(update, context)
    elif data == "download_video":
        await query.message.reply_text(
            "📥 ارسل رابط فيديو تيك توك لتحميله:"
        )
    elif data == "my_stats":
        await stats_command(update, context)
    elif data == "unlike_all":
        await unlike_all_command(update, context)
    elif data == "search_user":
        await query.message.reply_text(
            "🔍 ارسل اسم المستخدم للبحث (بدون @):"
        )
    elif data == "extract_links":
        await extract_links_command(update, context)
    elif data == "logout":
        await logout_command(update, context)
    elif data == "help":
        await help_command(update, context)
    elif data == "confirm_unlike":
        await confirm_unlike(update, context)
    elif data == "cancel_unlike":
        await cancel_unlike(update, context)
    elif data == "back_start":
        await query.message.reply_text(
            "اضغط /start لعرض القائمة الرئيسية."
        )

    # ─── Admin Actions ────────────────
    elif data == "admin_panel":
        await admin_panel_command(update, context)
    elif data == "admin_stats":
        await admin_stats_handler(update, context)
    elif data == "admin_users":
        await admin_users_handler(update, context)
    elif data == "admin_sessions":
        await admin_sessions_handler(update, context)
    elif data == "admin_activity":
        await admin_activity_handler(update, context)
    elif data == "admin_broadcast":
        await query.message.reply_text(
            "📢 *اذاعة رسالة*\n\n"
            "استخدم امر /broadcast لارسال رسالة جماعية.",
            parse_mode="Markdown",
        )
    elif data == "admin_ban":
        await query.message.reply_text(
            "🚫 *حظر مستخدم*\n\n"
            "استخدم امر /ban لحظر مستخدم.",
            parse_mode="Markdown",
        )
    elif data == "admin_unban":
        await admin_unban_handler(update, context)
    elif data == "admin_banned_list":
        await admin_banned_list_handler(update, context)
    elif data == "admin_restart":
        await admin_restart_handler(update, context)
    elif data == "admin_clear_data":
        await admin_clear_data_handler(update, context)
    elif data == "confirm_clear":
        if is_admin(user.id):
            user_sessions.clear()
            user_activity.clear()
            bot_stats["total_commands"] = 0
            bot_stats["total_downloads"] = 0
            bot_stats["total_reposts_deleted"] = 0
            bot_stats["total_unlikes"] = 0
            bot_stats["total_extracts"] = 0
            bot_stats["total_session_extracts"] = 0
            await query.message.reply_text("✅ تم مسح جميع البيانات بنجاح.")
    elif data == "confirm_restart":
        if is_admin(user.id):
            await query.message.reply_text(
                "🔄 جاري اعادة التشغيل...\n"
                "البوت سيعود خلال ثوان."
            )
            # In production, you'd use a process manager to restart
            os._exit(0)
    elif data.startswith("do_unban_"):
        if is_admin(user.id):
            try:
                target_id = int(data.replace("do_unban_", ""))
                banned_users.discard(target_id)
                await query.message.reply_text(
                    f"✅ تم الغاء حظر المستخدم `{target_id}`.",
                    parse_mode="Markdown",
                )
                # Notify the user
                try:
                    await context.bot.send_message(
                        chat_id=target_id,
                        text="✅ تم الغاء حظرك! يمكنك استخدام البوت مجددا.\nاضغط /start",
                    )
                except Exception:
                    pass
            except ValueError:
                pass


# ─── Cancel Handler ────────────────────────────────────────────
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current conversation."""
    await update.message.reply_text(
        "❌ تم الالغاء.\nاضغط /start للعودة للقائمة."
    )
    return ConversationHandler.END


# ─── Main ──────────────────────────────────────────────────────
def main():
    """Start the bot."""
    if BOT_TOKEN == "8528289566:AAEmPyaxSVBSiAMP9FTxOmKJnVXGzxZ_RGo":
        print("=" * 50)
        print("  ERROR: Please set your Telegram Bot Token!")
        print("")
        print("  Set the TELEGRAM_BOT_TOKEN environment variable:")
        print("    export TELEGRAM_BOT_TOKEN='your_token_here'")
        print("")
        print("  Set your admin ID:")
        print("    export ADMIN_USER_ID='your_telegram_id'")
        print("")
        print("  Or edit the variables in this script.")
        print("=" * 50)
        sys.exit(1)

    if ADMIN_USER_ID == 5154904380:
        print("WARNING: ADMIN_USER_ID not set! Admin panel will be disabled.")
        print("Set it via: export ADMIN_USER_ID='your_telegram_id'")

    # Build application
    app = Application.builder().token(BOT_TOKEN).build()

    # ─── Conversation Handlers ─────────────────────────────
    login_handler = ConversationHandler(
        entry_points=[
            CommandHandler("login", login_command),
        ],
        states={
            WAITING_SESSION_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_session_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    download_handler = ConversationHandler(
        entry_points=[
            CommandHandler("download", download_command),
        ],
        states={
            WAITING_VIDEO_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_video_url)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    search_handler = ConversationHandler(
        entry_points=[
            CommandHandler("user_info", search_user_command),
        ],
        states={
            WAITING_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_username)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    extract_handler = ConversationHandler(
        entry_points=[
            CommandHandler("extract_links", extract_links_command),
        ],
        states={
            WAITING_EXTRACT_USERNAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_extract_username
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    broadcast_handler = ConversationHandler(
        entry_points=[
            CommandHandler("broadcast", admin_broadcast_start),
        ],
        states={
            WAITING_BROADCAST_MSG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_broadcast_message)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    ban_handler = ConversationHandler(
        entry_points=[
            CommandHandler("ban", admin_ban_start),
        ],
        states={
            WAITING_BAN_USER_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_ban_user_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # ─── Register Handlers ─────────────────────────────────
    app.add_handler(login_handler)
    app.add_handler(download_handler)
    app.add_handler(search_handler)
    app.add_handler(extract_handler)
    app.add_handler(broadcast_handler)
    app.add_handler(ban_handler)

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("session", session_extract_command))
    app.add_handler(CommandHandler("delete_reposts", delete_reposts_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("unlike_all", unlike_all_command))
    app.add_handler(CommandHandler("logout", logout_command))
    app.add_handler(CommandHandler("check_session", check_session_command))
    app.add_handler(CommandHandler("admin", admin_panel_command))

    app.add_handler(CallbackQueryHandler(button_callback))

    # ─── Start Bot ─────────────────────────────────────────
    print("=" * 50)
    print("  TikTok Tools Bot is running!")
    print(f"  Admin ID: {ADMIN_USER_ID}")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
