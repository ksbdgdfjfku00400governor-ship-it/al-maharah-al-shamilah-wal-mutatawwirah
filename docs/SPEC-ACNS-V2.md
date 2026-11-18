# Spec: ACNS v2.0 — Resource Intelligence

## Objective
إضافة طبقة استخبارات موارد مستقلة فوق النواة المشتركة، مع الحفاظ على قابلية تشغيل v1. يكتشف النظام الموارد المرئية فعليًا، يسجل قدراتها، يقيّمها، يفرض الصلاحيات، ويختار بديلًا عند الفشل.

## Interfaces

- `ResourceDiscovery.discover() -> Iterable[Resource]`
- `ResourceRegistry.register/get/all`
- `CapabilityResolver.resolve(resources, required) -> list[ResourceCandidate]`
- `PermissionManager.can_use(resource) -> bool`
- `ResourceAdapter.use(resource, payload) -> dict`
- `FallbackManager.choose(candidates, excluded) -> ResourceCandidate | None`
- `ResourceIntelligenceEngine.discover/select/best`
- `VersionManager.register/select/current/compatibility`

## Boundaries

- يعمل دون اتصال خارجي افتراضيًا.
- لا يحمّل موارد غير مطلوبة.
- لا يمنح صلاحيات لمجرد اكتشاف المورد.
- لا يحذف أو يستبدل v1.
- لا يضيف تعلمًا ذاتيًا غير مقاس.

## Success Criteria

1. يختار المحرك موردًا محليًا مصرحًا عند تلبية القدرات المطلوبة.
2. يستبعد الموارد غير المسموح بها.
3. يختار بديلًا بعد استبعاد المورد الفاشل.
4. يسمح مدير الإصدارات باختيار v1 أو v2 دون تحميل الآخر.
5. تنجح اختبارات v1 وv2 معًا.
6. لا يحتاج التشغيل الأساسي إلى الإنترنت.
