# ACNS — النظام العصبي المعرفي للذكاء الاصطناعي

**AI Cognitive Neural System** هو نموذج حوسبي محلي مستوحى من تنظيم الخلايا العصبية. ليس دماغًا بيولوجيًا ولا يدّعي وعيًا أو تعلمًا ذاتيًا حقيقيًا؛ بل يثبت تنسيق الإدراك والذاكرة والاستدلال والتخطيط والتنفيذ والمراقبة والنقد والتعلم المصرح به.

## التشغيل دون إنترنت

يتطلب Python 3.10+ فقط للتشغيل الأساسي:

```bash
PYTHONPATH=src python -m acns.demo
```

للاختبارات:

```bash
python -m pytest -q
```

## البنية

- `src/acns/core`: النواة المعرفية.
- `src/acns/cells`: الخلايا العشر المستقلة.
- `src/acns/memory`: واجهة ذاكرة مجردة وتنفيذ SQLite.
- `src/acns/communication`: بروتوكول الرسائل وقناة الإشارات.
- `src/acns/security`: خلية الحماية المستقلة.
- `src/acns/resource_intelligence`: محرك استخبارات الموارد في v2.
- `src/acns/version_manager.py`: اختيار الإصدار والتوافق دون تحميل إصدارات أخرى.
- `versions/v1` و`versions/v2`: توثيق الإصدارات المستقلة المحتفظ بها.
- `tests`: اختبارات وحدات وتكامل وقبول.
- `docs`: مواصفة ومعمارية وبروتوكولات.
- `SKILL.md`: المهارة المركزية المستقلة، وتظل قابلة للاستخدام دون تشغيل ACNS.

## حدود V1

لا توجد اتصالات خارجية أو نماذج لغوية أو تعديل ذاتي للكود. التعلم في V1 استخراج دروس قابلة للقياس، ولا يُحفظ إلا بإذن صريح في سياق المهمة.

## V2 — Resource Intelligence

يضيف v2 اكتشاف الموارد المحلية، سجل الموارد، حل القدرات، تقييم الصلة والموثوقية والتكلفة والزمن، إدارة الصلاحيات، والبدائل عند تعذر مورد. يعمل المحرك دون إنترنت افتراضيًا ولا يحمّل الموارد إلا عند الحاجة. يبقى v1 قابلًا للتشغيل ولا يتم استبداله أو تحميل v2 تلقائيًا.

```python
from acns.resource_intelligence import Resource, ResourceIntelligenceEngine

engine = ResourceIntelligenceEngine()
engine.registry.register(Resource("local-parser", "local", "Parser", frozenset({"parse"})))
candidate = engine.best({"parse"})
```
