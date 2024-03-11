# Migrations

---

Для работы с миграциями используется библиотека `alembic`

С более подробной информацией можно ознакомиться в официальной 
[документации](https://alembic.sqlalchemy.org/en/latest/index.html).

---

## Создание миграции

Для создания миграции c применением авто генерации кода нужно использовать команду:

```shell
alembic revision --autogenerate -m "<msg>"
```
Где `msg` это сообщение миграции

Для создания миграции без авто генерации необходимо запускать создание миграций без флага `--autogenerate`

***Важно! При использовании авто генерации кода нужно проверять созданные миграции и, в случае необходимости, 
дорабатывать их вручную.***

После успешного создания миграции, она сохранится в директории `migration/versions/` со следующим содержанием:

```python
"""Create notification table # Сообщение миграции

Revision ID: 841d6bb63133 # Идентификатор миграции
Revises: 1a2b34cd5e67 # идентификатор предыдущей миграции
Create Date: 2024-02-07 21:18:26.806788 # Дата и время создания миграции

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '841d6bb63133'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Действия для применения миграций
    ... 


def downgrade() -> None:
    # Действия для отката миграций 
    ...

```

---

## Применение конкретной миграции

Для применения конкретной миграции необходимо после `upgrade` указать `revision` миграции, значение которой находится в 
файле необходимой миграции в директории `migration/versions/...`.

```shell
alembic upgrade <migration revision>
```

### Пример

`./migration/versions/1a2b34cd5e67.py`

```python
...
# revision identifiers, used by Alembic.
revision = '1a2b34cd5e67'
down_revision = None
branch_labels = None
depends_on = None
...
```

```shell
alembic upgrade 1a2b34cd5e67
```

---

## Применение последних миграций

```shell
alembic upgrade head
```

---

## Откат конкретной миграции

Для применения конкретной миграции необходимо после `upgrade` указать `revision` миграции, значение которой находится в 
файле необходимой миграции в директории `migration/versions/...`.

```shell
alembic downgrade <migration revision>
```

### Пример

`./migration/versions/1a2b34cd5e67.py`

```python
...
# revision identifiers, used by Alembic.
revision = '1a2b34cd5e67'
down_revision = None
branch_labels = None
depends_on = None
...
```

```shell
alembic downgrade 1a2b34cd5e67
```

---

## Откат всех миграций

```shell
alembic downgrade base
```
