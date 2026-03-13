const { Telegraf, Markup } = require('telegraf');
const bot = new Telegraf(process.env.BOT_TOKEN);

const SMART_LINK = process.env.SMART_LINK;

// স্টার্ট কমান্ড
bot.start((ctx) => {
    const message = ctx.update.message.text;
    const fileId = message.split(' ')[1];

    if (fileId) {
        ctx.reply('⚠️ ভিডিওটি লক করা আছে! আনলক করতে নিচের বাটনে ক্লিক করে অ্যাড দেখুন।', 
            Markup.inlineKeyboard([
                [Markup.button.url('🔗 Watch Ad to Unlock', SMART_LINK)],
                [Markup.button.callback('✅ I have Watched', `unlock:${fileId}`)]
            ])
        );
    } else {
        ctx.reply('স্বাগতম! ভিডিওর জন্য চ্যানেলে যান।');
    }
});

// আনলক লজিক
bot.on('callback_query', async (ctx) => {
    const data = ctx.callbackQuery.data;
    if (data.startsWith('unlock:')) {
        const fileId = data.split(':')[1];
        await ctx.answerCbQuery('ভিডিও পাঠানো হচ্ছে...');
        await ctx.deleteMessage();
        await ctx.replyWithVideo(fileId, { caption: '✅ আপনার ভিডিওটি আনলক হয়েছে!' });
    }
});

// এডমিন ভিডিও দিলে বাটন লিংক তৈরি করা
bot.on('video', (ctx) => {
    if (ctx.chat.type === 'private') {
        const fileId = ctx.message.video.file_id;
        ctx.reply(`আপনার ভিডিও বাটন লিংক:\n\nhttps://t.me/${ctx.botInfo.username}?start=${fileId}`);
    }
});

bot.launch();
console.log("Bot is running...");
