# بروتوكول الاتصال

تستخدم الخلايا كائن `Signal` موحدًا يحتوي على:

`message_id`, `source`, `destination`, `signal_type`, `task_id`, `content`, `source_ref`, `confidence`, `status`, `timestamp`.

`SignalBus.send()` يمنع الرسالة المكررة، و`receive()` يعيد رسائل الوجهة أو المهمة المطلوبة. يحتفظ السجل الكامل في `history` لتتبع علاقة القرارات بالنتائج. في V1 القناة داخل العملية، لكنها مفصولة بما يكفي لاستبدالها بطابور موزع لاحقًا.
