# الخلايا المعرفية — Cognitive Cells

كل خلية تطبق `CognitiveCell.process(state) -> CellResult`، وتعيد أدلة وأخطاء قابلة للمراجعة. الخلية لا تتجاوز مسؤوليتها ولا تعتمد على اتصال إنترنت.

| الخلية | الواجهة | السلوك القابل للاختبار |
|---|---|---|
| PerceptionCell | `process(TaskState)` | تستخرج النية والكلمات وتبلغ عن الطلب الفارغ |
| MemoryCell | `process(TaskState)` | تسترجع مطابقات من `MemoryStore` |
| ReasoningCell | `process(TaskState)` | تتطلب نجاح الإدراك وتفصل المعلوم عن الافتراض والمجهول |
| PlanningCell | `process(TaskState)` | تنتج خطوات وتبعيات مرتبة |
| ExecutionCell | `process(TaskState)` | تنفذ المسار المحلي وتعيد خطأً قابلًا لإعادة التخطيط |
| MonitoringCell | `process(TaskState)` | ترصد الخلايا الفاشلة وعدد الأحداث |
| CriticCell | `process(TaskState)` | تراجع وجود الأدلة بصورة مستقلة |
| LearningCell | `process(TaskState)` | تستخرج درسًا وتحفظه فقط عند `allow_learning` |
| CreativityCell | `process(TaskState)` | تولد مسارات بديلة دون اعتمادها تلقائيًا |
| SecurityCell | `process(TaskState)` | تحجب مؤشرات الحقن أو العمليات الخطرة قبل بقية الخلايا |

إضافة خلية جديدة لا تتطلب تغيير الذاكرة أو بروتوكول الرسائل؛ يكفي تطبيق الواجهة وتسجيلها في النواة مع اختبار مستقل.
