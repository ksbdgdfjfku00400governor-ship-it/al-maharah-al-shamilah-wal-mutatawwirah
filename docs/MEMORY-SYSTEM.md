# نظام الذاكرة

`MemoryStore` هو الحد الفاصل بين الخلايا والتخزين. يوفر:

- `put(key, value, memory_type, source, confidence)` للحفظ مع المصدر والثقة.
- `search(query, memory_type, limit)` للاسترجاع المحلي.
- `forget(key)` لطلبات النسيان.

`SQLiteMemoryStore` هو التنفيذ الأول ويعمل داخل الذاكرة أو في ملف SQLite. أنواع الذاكرة المستخدمة في V1 هي `working`, `episodic`, `semantic`, و`procedural` بحسب سياق الاستدعاء. لا تُعامل النتائج كحقائق مؤكدة؛ المصدر والثقة جزء من كل سجل.

يمكن لاحقًا إضافة موفر متجهات أو ملف دون تعديل `CognitiveCore` أو الخلايا.
