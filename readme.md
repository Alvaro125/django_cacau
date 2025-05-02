```md
myproject/
│
├── manage.py
├── myproject/               ← Configurações do Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── myapp/                   ← App principal
│   ├── __init__.py
│   ├── apps.py
│   ├── migrations/
│   ├── api/                 ← Interface com o mundo externo (views, serializers, routers)
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   │
│   ├── domain/              ← Regras de negócio (entidades, regras, interfaces)
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── services.py
│   │
│   ├── infrastructure/      ← Integrações externas (ORM, cache, fila, API externa etc.)
│   │   ├── __init__.py
│   │   └── repositories.py
│   │
│   ├── application/         ← Casos de uso (application layer)
│   │   ├── __init__.py
│   │   └── usecases.py
│   │
│   └── tests/               ← Testes organizados por camada
│       ├── __init__.py
│       ├── test_views.py
│       ├── test_usecases.py
│       └── test_models.py
```