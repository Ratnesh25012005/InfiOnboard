import os
import io
import telebot
from pypdf import PdfReader

# We import the exact same algorithm models we use on the website!
from main import process_nlp_extraction
from database import get_courses_for_skills

# The bot token you get from @BotFather on Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("🚀 InfiOnboard Telegram Bot is starting...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the InfiOnboard Mobile Engine!\n\nPlease send me a *Job Description* (paste it into the caption field) and attach your *Resume* (as a PDF document) to generate your AI-adaptive training path!", parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_resume(message):
    try:
        if not message.document.file_name.lower().endswith('.pdf'):
            bot.reply_to(message, "❌ Please attach a valid PDF document.")
            return

        jd_text = message.caption
        if not jd_text:
            bot.reply_to(message, "❌ Missing Job Description! Please resend your PDF and paste the Job Description text directly into the *Caption* bar before hitting send.", parse_mode='Markdown')
            return

        # Let the user know we are processing
        processing_msg = bot.reply_to(message, "⏳ _Analyzing Resume against Job Description..._", parse_mode='Markdown')

        # 1. Download PDF securely from Telegram Servers
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        pdf = PdfReader(io.BytesIO(downloaded_file))
        final_resume_text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

        # 2. Extract Skills
        resume_extracted = process_nlp_extraction(final_resume_text)
        jd_extracted = process_nlp_extraction(jd_text)
        
        skill_gap = set(jd_extracted.keys()) - set(resume_extracted.keys())

        if not skill_gap:
            bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text="🎉 *Perfect Match!*\n\nYour resume indicates you have all the required skills for this job! No additional training modules are required.", parse_mode='Markdown')
            return

        # 3. Build the Learning Pathway
        pathway = []
        seen_ids = set()
        
        for missing_skill in skill_gap:
            courses = get_courses_for_skills([missing_skill])
            for row in courses:
                if row["id"] not in seen_ids:
                    seen_ids.add(row["id"])
                    item = dict(row)
                    item["reasoning"] = f"Candidate lacks '{missing_skill.replace('_', ' ').title()}'. JD requires it."
                    pathway.append(item)
                    
        level_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
        pathway.sort(key=lambda c: level_order.get(c["level"], 99))
        total_hours = sum(c["duration_hours"] for c in pathway)

        # 4. Format Beautiful Telegram Output
        msg = f"🎯 *InfiOnboard Analysis Complete*\n\n"
        msg += f"🧩 *Skill Gaps Identified:* {len(skill_gap)}\n"
        msg += f"⏱ *Total Pathway Duration:* {total_hours}h\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += "🛤️ *YOUR CUSTOM TIMELINE*\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, c in enumerate(pathway[:5]):
            icon = "▶️" if c["resource_type"] == "Video" else "📄" if c["resource_type"] == "Documentation" else "💻"
            msg += f"{i+1}️⃣ *{c['title']}*\n"
            msg += f"🏅 *Level:* {c['level']} | ⏱ *Time:* {c['duration_hours']}h\n"
            msg += f"_{c['description']}_\n"
            msg += f"💡 *Reasoning:* {c['reasoning']}\n"
            msg += f"{icon} [Access {c['resource_type']}]({c['resource_link']})\n\n"
            
        if len(pathway) > 5:
            msg += f"➕ _...and {len(pathway)-5} more advanced modules!_\n"

        # Overwrite the "processing..." message with the final timeline
        bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text=msg.strip(), parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Oops! Something went wrong analyzing your profile: {str(e)}")

# This starts the Long-Polling! It will listen securely without needing ngrok!
if __name__ == "__main__":
    if TELEGRAM_TOKEN == "PUT_YOUR_TOKEN_HERE":
        print("ERROR: You must insert your Telegram Bot Token on line 9 of this file to start the bot!")
    else:
        print("✅ Telegram Bot is actively listening for incoming Resumes!")
        bot.infinity_polling()
